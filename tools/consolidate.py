#!/usr/bin/env python3
"""
True consolidation of multiple skill sources into a single deduplicated,
best-practice layout:

    skills/<category>/<unit>/            one dir per skill unit (composites intact)
    agents/  commands/  standards/  templates/  docs/  tools/
    skills-index.json                    machine-readable catalog
    sources.lock.json                    source repos pinned to commit SHAs
    CONSOLIDATION.md                     per-decision log (kept/skipped/why)

Sources (override paths via env):
    SRC_CLAUDE_SKILLS     alirezarezvani/claude-skills fork          (MIT)
    SRC_MP_SKILLS         mattpocock/skills                          (MIT)
    SRC_SUPERPOWERS       obra/superpowers                           (MIT)
    SRC_ANTHROPIC_SKILLS  anthropics/skills (Apache-2.0 picks only)

Dedup rules:
  R1  Same unit name, SKILL.md byte-identical  -> keep one copy
      (prefer the original author's copy, else the richer dir).
  R2  Stale forks of original-author skills inside claude-skills -> keep the
      original author's current version.
  R3  Same name but genuinely different skills -> keep both in different
      categories; collision recorded in the index.
  R4  Sub-skills of different composites sharing names -> no conflict:
      composites are kept as single units.

Run:  python3 tools/consolidate.py   (from the repo root)
"""

import hashlib
import json
import os
import re
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HOME = Path.home()
VENDOR_CS = Path(os.getenv("SRC_CLAUDE_SKILLS", str(HOME / ".claude" / "claude-skills")))
VENDOR_MP = Path(os.getenv("SRC_MP_SKILLS", str(HOME / ".claude" / "mattpocock-skills")))
OUT_SKILLS = ROOT / "skills"

# Flat `skills/<name>/` sources added 2026-07-14 after the ecosystem research
# (docs/ECOSYSTEM.md): superpowers = methodology layer; anthropics picks are the
# Apache-2.0 engineering skills only (the docx/pdf/pptx/xlsx skills are
# source-available, NOT open source -> never ingest them).
EXTRA_SOURCES = [
    {
        "source": "superpowers",
        "root": Path(os.getenv("SRC_SUPERPOWERS", str(HOME / ".claude" / "superpowers"))),
        "category": "methodology",
        "include": None,  # all
        "license": "MIT",
    },
    {
        "source": "anthropic-skills",
        "root": Path(os.getenv("SRC_ANTHROPIC_SKILLS", str(HOME / ".claude" / "anthropic-skills"))),
        "category": "engineering",
        "include": {"skill-creator", "mcp-builder", "webapp-testing", "claude-api", "frontend-design"},
        "license": "Apache-2.0 (per-skill LICENSE.txt)",
    },
]

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
# Test fixtures shipped by upstream, not real skills
FIXTURE_UNITS = {"sample-skill"}
# R2: both claude-skills handoff variants are expanded forks of mattpocock's handoff
CS_SKIP_UNIT_PATHS = {"engineering/handoff", "productivity/handoff"}


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
    """Return (unit_root, unit_name) for a claude-skills SKILL.md path."""
    rel = skill_md.relative_to(vendor_root)
    parts = rel.parts
    if len(parts) >= 4 and parts[-3] == "skills" and len(parts) == 4:
        return vendor_root / parts[0] / "skills" / parts[2], parts[2]
    if len(parts) >= 5 and parts[-3] == "skills":
        return vendor_root / parts[0] / parts[1], parts[1]
    if len(parts) == 3:
        return vendor_root / parts[0] / parts[1], parts[1]
    return skill_md.parent, skill_md.parent.name


def collect_units():
    units = {}  # str(unit_root) -> dict
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
                    continue
                unit_root, unit_name = unit_for(smd, vendor_root)
                category = CS_CATEGORY_MAP[rel0]
            u = units.setdefault(str(unit_root), {
                "root": unit_root, "src_root": vendor_root, "name": unit_name,
                "source": which, "category": category, "skill_mds": [],
            })
            u["skill_mds"].append(smd)
    for ex in EXTRA_SOURCES:
        base = ex["root"] / "skills"
        if not base.exists():
            print(f"WARNING: extra source missing, skipped: {base}")
            continue
        for smd in sorted(base.rglob("SKILL.md")):
            top = smd.relative_to(base).parts[0]
            if ex["include"] is not None and top not in ex["include"]:
                continue
            unit_root = base / top
            u = units.setdefault(str(unit_root), {
                "root": unit_root, "src_root": ex["root"], "name": top,
                "source": ex["source"], "category": ex["category"], "skill_mds": [],
            })
            u["skill_mds"].append(smd)
    return list(units.values())


ORIGINAL_AUTHOR_ORDER = {"mattpocock-skills": 0, "superpowers": 1, "anthropic-skills": 2,
                         "claude-skills": 3}


def main():
    if OUT_SKILLS.exists():
        shutil.rmtree(OUT_SKILLS)
    units = collect_units()
    log, index, taken = [], [], {}
    # Original authors first so their copies win ties; then by name.
    units.sort(key=lambda u: (ORIGINAL_AUTHOR_ORDER.get(u["source"], 9), u["name"]))

    by_name = {}
    for u in units:
        by_name.setdefault(u["name"], []).append(u)

    for u in units:
        rel_unit = f'{u["source"]}/{u["root"].relative_to(u["src_root"])}'
        src_rel = str(u["root"].relative_to(u["src_root"]))
        name, cat, src = u["name"], u["category"], u["source"]

        if name in FIXTURE_UNITS:
            log.append(f"- SKIP `{rel_unit}` — upstream test fixture, not a skill")
            continue
        if src == "claude-skills" and name in CS_STALE_FORKS:
            log.append(f"- SKIP `{rel_unit}` — stale fork of mattpocock's `{name}` (R2); kept the original author's current version")
            continue
        if src == "claude-skills" and src_rel in CS_SKIP_UNIT_PATHS:
            log.append(f"- SKIP `{rel_unit}` — expanded fork of mattpocock's `{name}`; original author's current version kept (R2)")
            continue

        # R1: byte-identical to an already-placed unit of the same name
        skipped_r1 = False
        for other_key, other in taken.items():
            if other_key[1] != name:
                continue
            mine = u["skill_mds"][0].read_text(errors="replace")
            theirs = other["skill_mds"][0].read_text(errors="replace")
            if hashlib.md5(mine.encode()).hexdigest() == hashlib.md5(theirs.encode()).hexdigest():
                log.append(f"- SKIP `{rel_unit}` — byte-identical to kept `{other_key[0]}/{name}` (R1)")
                skipped_r1 = True
                break
        if skipped_r1:
            continue

        dest = OUT_SKILLS / cat / name
        if dest.exists():
            log.append(f"- SKIP `{rel_unit}` — name collision with already-kept `{cat}/{name}` (first-kept wins; review manually)")
            continue
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(u["root"], dest)
        prior = [k for k in taken if k[1] == name]
        if prior:
            log.append(f"- KEEP BOTH `{cat}/{name}` and `{prior[0][0]}/{name}` — same name, different skills (R3)")
        taken[(cat, name)] = u
        n, d = fm(u["skill_mds"][0].read_text(errors="replace"))
        index.append({
            "name": n or name, "category": cat, "path": f"skills/{cat}/{name}",
            "source": src, "description": d,
            "composite": len(u["skill_mds"]) > 1, "sub_skills": len(u["skill_mds"]),
            "has_scripts": bool(list(dest.rglob("scripts"))),
        })

    # non-skill assets from claude-skills
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
    for ex in EXTRA_SOURCES:
        src_lic = ex["root"] / "LICENSE"
        if src_lic.exists():
            shutil.copy2(src_lic, lic / f"LICENSE-{ex['source']}")
    # anthropic skills carry per-skill LICENSE.txt (Apache-2.0), retained by copytree

    # provenance lock
    lock = {}
    roots = {"claude-skills": VENDOR_CS, "mattpocock-skills": VENDOR_MP}
    roots.update({ex["source"]: ex["root"] for ex in EXTRA_SOURCES})
    for src_name, root in roots.items():
        try:
            sha = subprocess.run(["git", "-C", str(root), "rev-parse", "HEAD"],
                                 capture_output=True, text=True, check=True).stdout.strip()
            origin = subprocess.run(["git", "-C", str(root), "remote", "get-url", "origin"],
                                    capture_output=True, text=True, check=True).stdout.strip()
        except Exception:
            sha, origin = "unknown", "unknown"
        lock[src_name] = {"origin": origin, "commit": sha}
    (ROOT / "sources.lock.json").write_text(json.dumps(lock, indent=2) + "\n")

    index.sort(key=lambda e: (e["category"], e["name"]))
    (ROOT / "skills-index.json").write_text(json.dumps(index, indent=2) + "\n")

    header = (
        "# Consolidation log\n\n"
        f"Units kept: **{len(index)}** · decisions below. Rules: R1 byte-identical dedup · "
        "R2 stale/expanded forks dropped in favor of the original author's current version · "
        "R3 same-name different-skill kept in separate categories · R4 composite units kept "
        "intact (sub-skill name overlap is not a conflict).\n\n"
        "Sources (pinned in `sources.lock.json`): alirezarezvani/claude-skills (MIT) · "
        "mattpocock/skills (MIT) · obra/superpowers (MIT) · anthropics/skills "
        "(Apache-2.0 picks only — the source-available docx/pdf/pptx/xlsx skills are never "
        "ingested). mattpocock `deprecated/`, `in-progress/`, `personal/` excluded by policy.\n\n"
        "## Decisions\n\n"
    )
    (ROOT / "CONSOLIDATION.md").write_text(header + "\n".join(sorted(set(log))) + "\n")
    print(f"kept units: {len(index)}; logged decisions: {len(set(log))}")
    print(f"categories: {sorted({e['category'] for e in index})}")


if __name__ == "__main__":
    main()
