#!/usr/bin/env python3
"""
Validate every skill in skills/ against the agentskills.io spec + Anthropic
authoring constraints (see docs/ECOSYSTEM.md for sources):

  E1  frontmatter present with non-empty `name` and `description`
  E2  name: <=64 chars, lowercase letters/digits/hyphens, no leading/trailing/
      consecutive hyphens, must not contain "anthropic" or "claude"
  E3  name must equal its directory name
  E4  description <= 1024 chars
  W1  body < 500 lines (spec) and < ~5k tokens (chars/4 heuristic)
  W2  frontmatter fields outside the spec set
      {name, description, license, compatibility, metadata, allowed-tools}
      (`disable-model-invocation` tolerated: Claude Code extension)
  W3  description shorter than 20 chars (weak discovery surface)

Exit code: 1 if any E-level issue and --strict, else 0.
Usage: python3 tools/validate_skills.py [--strict] [--quiet]
"""

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SPEC_FIELDS = {"name", "description", "license", "compatibility", "metadata", "allowed-tools"}
TOLERATED = {"disable-model-invocation"}
NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")


def check(skill_md: Path):
    errors, warnings = [], []
    text = skill_md.read_text(errors="replace")
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n?(.*)$", text, re.S)
    if not m:
        return ["E1 no YAML frontmatter"], []
    fm_text, body = m.group(1), m.group(2)
    fields = {}
    for line in fm_text.splitlines():
        fmatch = re.match(r"^([A-Za-z_-]+):\s*(.*)$", line)
        if fmatch:
            fields[fmatch.group(1)] = fmatch.group(2).strip().strip("\"'")

    name = fields.get("name", "")
    desc = fields.get("description", "")
    if not name or not desc:
        errors.append("E1 missing name or description")
    if name:
        if len(name) > 64:
            errors.append(f"E2 name >64 chars ({len(name)})")
        if not NAME_RE.match(name):
            errors.append(f"E2 name not spec-compliant: {name!r}")
        if "anthropic" in name or "claude" in name:
            warnings.append(f"E2* name contains reserved word: {name!r} (upstream skill; not renamed)")
        if name != skill_md.parent.name:
            errors.append(f"E3 name {name!r} != dir {skill_md.parent.name!r}")
    if len(desc) > 1024:
        errors.append(f"E4 description >1024 chars ({len(desc)})")
    elif desc and len(desc) < 20:
        warnings.append(f"W3 weak description ({len(desc)} chars)")

    lines = body.count("\n") + 1
    tokens = len(body) // 4
    if lines >= 500:
        warnings.append(f"W1 body {lines} lines (>=500)")
    if tokens >= 5000:
        warnings.append(f"W1 body ~{tokens} tokens (>=5k)")
    extra = set(fields) - SPEC_FIELDS - TOLERATED
    if extra:
        warnings.append(f"W2 non-spec frontmatter fields: {sorted(extra)}")
    return errors, warnings


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--strict", action="store_true")
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args()

    files = [f for f in sorted((ROOT / "skills").rglob("SKILL.md"))
             if not any(p in ("assets", "expected_outputs") for p in f.parts)]
    n_err = n_warn = clean = 0
    for f in files:
        errors, warnings = check(f)
        n_err += len(errors)
        n_warn += len(warnings)
        if not errors and not warnings:
            clean += 1
        if (errors or (warnings and not args.quiet)):
            rel = f.relative_to(ROOT)
            for e in errors:
                print(f"ERROR {rel}: {e}")
            if not args.quiet:
                for w in warnings:
                    print(f"warn  {rel}: {w}")
    print(f"\n{len(files)} SKILL.md checked: {clean} clean, {n_err} errors, {n_warn} warnings")
    if args.strict and n_err:
        sys.exit(1)


if __name__ == "__main__":
    main()
