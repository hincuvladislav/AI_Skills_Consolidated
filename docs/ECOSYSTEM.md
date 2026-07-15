# AI Skills Ecosystem — Research Notes & Library Policy

**Researched 2026-07-14** (multi-agent web survey; load-bearing claims re-verified
against primary sources). This document records why the library is shaped the way it
is, and what to watch in the ecosystem.

## The standard

- **agentskills.io spec** (https://agentskills.io/specification, governed at
  https://github.com/agentskills/agentskills): SKILL.md with YAML frontmatter;
  **`name` must equal the parent directory name**, ≤64 chars, lowercase/digits/
  hyphens; `description` ≤1024 chars; only optional fields: `license`,
  `compatibility`, `metadata` (string map — versioning goes here), `allowed-tools`.
  Reference validator: `skills-ref`.
- **Anthropic authoring guidance**
  (https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices):
  body **<500 lines AND <5k tokens**; descriptions in third person with explicit
  trigger keywords ("a little bit pushy" — models undertrigger); file references one
  level deep; TOC for reference files >100 lines; **evals before docs** (≥3, paired
  with/without-skill baselines).
- **Vendor-neutral install path convergence:** `.agents/skills` /
  `~/.agents/skills` is honored by Codex, Cursor, Copilot, Gemini CLI, Goose,
  OpenCode, VS Code and others; `.claude/skills` remains a compatibility path.
  This repo's `skills/<category>/` layout is exactly what `npx skills add`
  (skills.sh) scans.

## Why curation beats aggregation (library policy)

1. **SkillsBench** (https://arxiv.org/abs/2602.12670): curated skills +16.6pp task
   pass rate; self-generated/exhaustive bundles −1.3pp; **focused skills beat
   exhaustive bundles**.
2. **Claude Code skill-listing budget** (https://code.claude.com/docs/en/skills):
   descriptions capped at ~1% of context by default; on overflow, least-invoked
   skills silently lose their descriptions and stop auto-triggering (observed: 63
   installed → 42 visible, issue anthropics/claude-code#13099). **Do NOT install all
   334 units into one agent.** Install per-domain, use semantic search
   (`tools/search_skills.sh`) for discovery, and tier rarely-used skills
   (`disable-model-invocation: true`, `skillOverrides: "name-only"`).
3. **Supply-chain reality:** ClawHub incident Feb 2026 — 341/2,857 skills malicious
   (11.9%, "ClawHavoc" campaign, Atomic Stealer); Snyk "ToxicSkills": 36.82% of
   scanned skills had ≥1 security flaw (2.6% prompt injection), and one community
   "skill scanner" was itself malware. Policy here: **pinned sources only**
   (pins in `MAINTAINERS.md`), no open contributions, review before adding a source, and
   prefer LLM-intent analysis over regex if scanning is ever automated.

## Sources & candidates

Input repositories, license mapping, pinned commits, ingestion scope, and the
evaluated-but-not-ingested candidate list live in the maintainers-only provenance
file: [`MAINTAINERS.md`](../MAINTAINERS.md). Everywhere else in the repo, inputs
are referenced by opaque ids (s1..s4, local).

## Quality tooling adopted / available

- `tools/validate_skills.py` — local validator implementing the spec + Anthropic
  constraints (name==dir, name charset, description ≤1024, <500 lines/<5k tokens,
  non-spec frontmatter fields). Known upstream non-conformances (kept as-is, not
  ours to rewrite): `engineering/playwright-pro/skills/pw` (internal dir name),
  `research/litreview` (description 1161 chars).
- External validators worth knowing: `skills-ref` (spec reference), `skill-lint`
  (himself65, MIT), SkillCheck (getskillcheck.com), skillgrade (eval CI,
  mgechev/skillgrade), Anthropic skill-creator's eval harness (bundled — we ingest
  skill-creator, so it's in-tree at `skills/engineering/skill-creator/`).

## Maintenance checklist (when refreshing sources)

1. `git pull` each source clone; review upstream diff before consolidating.
2. `python3 tools/consolidate.py` (updates skills/, indexes, lockfile, decision log).
3. `python3 tools/validate_skills.py --quiet` — investigate new errors.
4. Re-index Qdrant: `tools/index_skills.py --recreate`.
5. Commit; the refreshed pins land in `MAINTAINERS.md` automatically.
