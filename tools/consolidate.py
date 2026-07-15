#!/usr/bin/env python3
"""
True consolidation of vendor/claude-skills + vendor/mattpocock-skills into a single
deduplicated, best-practice layout:

    skills/<category>/<unit>/            one dir per skill unit (composites intact)
    agents/  commands/  standards/  templates/  docs/  tools/
    skills-index.json                    machine-readable catalog
    CONSOLIDATION.md                     per-decision log (kept/skipped/why)

Dedup rules:
  R1  Same unit name, SKILL.md byte-identical  -> keep one copy
      (prefer mattpocock original for his set, else the richer dir).
  R2  Known stale forks of mattpocock originals inside claude-skills
      (grill-me, grill-with-docs) -> keep mattpocock's current version.
  R3  Same name but genuinely different skills (research, handoff) -> keep both in
      different categories; collision recorded in the index.
  R4  Sub-skills of different composites sharing names (init/run/status) -> no
      conflict: composites are kept as single units.

Run:  python3 tools/consolidate.py   (from the repo root)
"""

import hashlib
import os
import json
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VENDOR_CS = Path(os.getenv("SRC_CLAUDE_SKILLS", str(Path.home() / ".claude" / "claude-skills")))
VENDOR_MP = Path(os.getenv("SRC_MP_SKILLS", str(Path.home() / ".claude" / "mattpocock-skills")))
OUT_SKILLS = ROOT / "skills"

CS_CATEGORY_MAP = {
    "engineering": "engineering",
    "engineering-team": "engineering",
    "product-team": "product",
    "research": "research",
    "research-ops": "research-ops",
    "project-management": "project-management",
    "productivity": "productivity",
    "business-growth": "business",
    "business-operations": "business",
    "commercial": "business",
    "marketing-skill": "marketing",
    "marketing": "marketing",
    "finance": "finance",
    "compliance-os": "compliance",
    "c-level-advisor": "c-level",
    "ra-qm-team": "ra-qm",
    "markdown-html": "documents",
    "loop-library": "engineering",
}
MP_CATEGORY_MAP = {"engineering": "workflow", "productivity": "productivity", "misc": "misc"}
MP_SKIP_DIRS = {"deprecated", "in-progress", "personal"}

# R2: claude-skills units that are stale copies of mattpocock originals -> skip
CS_STALE_FORKS = {"grill-me", "grill-with-docs"}
# R3: claude-skills engineering/handoff is an older small variant; productivity/handoff
# is a distinct rich skill. Skip only the engineering one.
CS_SKIP_UNIT_PATHS = {"engineering/handoff"}


def fm(text):
    m = re.match(r"^---\s*\n(.*?)\n---", text, re.S)
    name = desc = ""
    if m:
        for line in m.group(1).splitlines():
            if line.startswith("name:"):
                name = line.split(":", 1)[1].strip().strip("\"'")
            elif line.startswith("description:"):
                desc = line.split(":", 1)[1].strip().strip("\"'")
    return name, desc


def unit_for(skill_md: Path, vendor_root: Path):
    """Return (unit_root, unit_name) for a SKILL.md path."""
    rel = skill_md.relative_to(vendor_root)
    parts = rel.parts
    # claude-skills layouts:
    #   <cat>/skills/<name>/SKILL.md            -> standalone
    #   <cat>/<plugin>/skills/<name>/SKILL.md   -> composite unit <plugin>
    #   <cat>/<name>/SKILL.md                   -> standalone
    #   <name>/SKILL.md                         -> standalone (rare)
    if len(parts) >= 4 and parts[-3] == "skills" and len(parts) == 4:
        return vendor_root / parts[0] / "skills" / parts[2], parts[2]
    if len(parts) >= 5 and parts[-3] == "skills":
        return vendor_root / parts[0] / parts[1], parts[1]
    if len(parts) == 3:
        return vendor_root / parts[0] / parts[1], parts[1]
    return skill_md.parent, skill_md.parent.name


def collect_units():
    units = {}  # unit_root -> dict
    for vendor_root, which in ((VENDOR_CS, "claude-skills"), (VENDOR_MP, "mattpocock-skills")):
        base = vendor_root if which == "claude-skills" else vendor_root / "skills"
        for smd in sorted(base.rglob("SKILL.md")):
            rel0 = smd.relative_to(base).parts[0]
            if which == "mattpocock-skills":
                if rel0 in MP_SKIP_DIRS:
                    continue
                unit_root, unit_name = smd.parent, smd.parent.name
                category = MP_CATEGORY_MAP.get(rel0, "misc")
            else:
                if rel0 not in CS_CATEGORY_MAP:
                    continue  # docs, templates, scripts, agents handled separately
                unit_root, unit_name = unit_for(smd, vendor_root)
                category = CS_CATEGORY_MAP[rel0]
            u = units.setdefault(str(unit_root), {
                "root": unit_root, "name": unit_name, "source": which,
                "category": category, "skill_mds": [],
            })
            u["skill_mds"].append(smd)
    return list(units.values())


def main():
    if OUT_SKILLS.exists():
        shutil.rmtree(OUT_SKILLS)
    units = collect_units()
    log, index, taken = [], [], {}  # taken: (category, name) -> unit
    # Sort: mattpocock first so his originals win ties; then by name.
    units.sort(key=lambda u: (u["source"] != "mattpocock-skills", u["name"]))

    by_name = {}
    for u in units:
        by_name.setdefault(u["name"], []).append(u)

    for u in units:
        rel_unit = ("claude-skills/" if u["source"] == "claude-skills" else "mattpocock-skills/") + str(u["root"].relative_to(VENDOR_CS if u["source"] == "claude-skills" else VENDOR_MP))
        cs_rel = "/".join(rel_unit.split("/")[1:])  # strip repo prefix
        name, cat, src = u["name"], u["category"], u["source"]

        if src == "claude-skills" and name in CS_STALE_FORKS:
            log.append(f"- SKIP `{rel_unit}` — stale fork of mattpocock's `{name}` (R2); kept the original author's current version")
            continue
        if src == "claude-skills" and cs_rel in CS_SKIP_UNIT_PATHS:
            log.append(f"- SKIP `{rel_unit}` — older small variant; kept richer `productivity/handoff` and mattpocock `workflow/handoff` (R3)")
            continue

        group = by_name[name]
        if len(group) > 1:
            mine = (u["skill_mds"][0].read_text(errors="replace"))
            for other in group:
                if other is u:
                    continue
                key = (other["category"], name)
                if key in [(k[0], k[1]) for k in taken if k[1] == name]:
                    theirs = other["skill_mds"][0].read_text(errors="replace")
                    if hashlib.md5(mine.encode()).hexdigest() == hashlib.md5(theirs.encode()).hexdigest():
                        # R1 byte-identical duplicate of an already-placed unit
                        n_mine = sum(1 for _ in u["root"].rglob("*") if _.is_file())
                        n_theirs = sum(1 for _ in other["root"].rglob("*") if _.is_file())
                        if n_mine <= n_theirs:
                            log.append(f"- SKIP `{rel_unit}` — byte-identical to kept `{other['category']}/{name}` (R1)")
                            break
            else:
                pass
            if any(l.endswith("(R1)") and f"`{rel_unit}`" in l for l in log):
                continue

        dest = OUT_SKILLS / cat / name
        if dest.exists():
            # same category+name from two sources and not identical -> keep first, log
            log.append(f"- SKIP `{rel_unit}` — name collision with already-kept `{cat}/{name}` (first-kept wins; review manually)")
            continue
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(u["root"], dest)
        taken[(cat, name)] = u
        n, d = fm(u["skill_mds"][0].read_text(errors="replace"))
        sub = len(u["skill_mds"])
        index.append({
            "name": n or name, "category": cat, "path": f"skills/{cat}/{name}",
            "source": src, "description": d,
            "composite": sub > 1, "sub_skills": sub,
            "has_scripts": any((dest / p).exists() for p in ("scripts",)) or bool(list(dest.rglob("scripts"))),
        })
        collide = [g for g in by_name[name] if g is not u and (g["category"], name) in taken]
        if collide:
            log.append(f"- KEEP BOTH `{cat}/{name}` and `{collide[0]['category']}/{name}` — same name, different skills (R3)")

    # non-skill assets
    for src_dir, dst in (("agents", "agents"), ("commands", "commands"),
                         ("standards", "standards"), ("templates", "templates")):
        s = VENDOR_CS / src_dir
        if s.exists():
            d = ROOT / dst
            if d.exists():
                shutil.rmtree(d)
            shutil.copytree(s, d)
    docs = ROOT / "docs"
    docs.mkdir(exist_ok=True)
    for f in ("SKILL-AUTHORING-STANDARD.md", "CONVENTIONS.md"):
        if (VENDOR_CS / f).exists():
            shutil.copy2(VENDOR_CS / f, docs / f)
    lic = ROOT / "LICENSES"
    lic.mkdir(exist_ok=True)
    shutil.copy2(VENDOR_CS / "LICENSE", lic / "LICENSE-claude-skills")
    shutil.copy2(VENDOR_MP / "LICENSE", lic / "LICENSE-mattpocock-skills")

    index.sort(key=lambda e: (e["category"], e["name"]))
    (ROOT / "skills-index.json").write_text(json.dumps(index, indent=2) + "\n")

    kept = len(index)
    header = (
        "# Consolidation log\n\n"
        f"Units kept: **{kept}** · decisions below. Rules: R1 byte-identical dedup · "
        "R2 stale forks of original-author skills dropped · R3 same-name different-skill kept in "
        "separate categories · R4 composite units kept intact (sub-skill name overlap is not a conflict).\n\n"
        "Sources: alirezarezvani/claude-skills v2.9.0 (MIT) · mattpocock/skills (MIT). "
        "mattpocock `deprecated/`, `in-progress/`, `personal/` excluded by policy.\n\n## Decisions\n\n"
    )
    (ROOT / "CONSOLIDATION.md").write_text(header + "\n".join(sorted(set(log))) + "\n")
    print(f"kept units: {kept}; logged decisions: {len(set(log))}")
    print(f"categories: {sorted({e['category'] for e in index})}")


if __name__ == "__main__":
    main()
