# AI Skills Consolidated

A **deduplicated, single-tree** consolidation of two agent-skills libraries, restructured
per current skill-repo best practices (one dir per skill unit, machine-readable index,
progressive disclosure: `SKILL.md` ≤500 lines + `scripts/` + `references/` + `assets/`).

| Source | License | Contribution |
|---|---|---|
| [alirezarezvani/claude-skills](https://github.com/alirezarezvani/claude-skills) v2.9.0 (via fork) | MIT © 2025 Alireza Rezvani | broad library (engineering → C-level) |
| [mattpocock/skills](https://github.com/mattpocock/skills) | MIT © 2026 Matt Pocock | composable engineering-workflow set |

**316 skill units · 370 SKILL.md files · 15 categories.** Duplicates resolved
skill-by-skill — every decision is logged in [`CONSOLIDATION.md`](CONSOLIDATION.md)
(rules: byte-identical dedup; stale forks dropped in favor of the original author's
current version; same-name-different-skill kept in separate categories; composite
skills kept intact).

## Layout

```
skills/<category>/<unit>/     # one dir per skill unit (SKILL.md [+ scripts|references|assets])
    engineering/  workflow/  product/  research/  research-ops/  project-management/
    productivity/ business/  marketing/ finance/  compliance/  c-level/  ra-qm/
    documents/    misc/
agents/                       # 99 role personas
commands/                     # slash-command definitions
standards/                    # process standards (communication, quality, git, docs, security)
templates/  docs/             # authoring standard & conventions
tools/                        # consolidation, Qdrant indexing, semantic search
skills-index.json             # machine-readable catalog: name·category·path·source·description
CONSOLIDATION.md              # dedup decision log
LICENSES/                     # upstream MIT notices (keep when redistributing)
```

Notes: `workflow/` is the mattpocock engineering set kept coherent (to-spec, to-tickets,
implement, code-review, triage, wayfinder, tdd, diagnosing-bugs, domain-modeling, …).
His `deprecated/`, `in-progress/`, `personal/` dirs were excluded by policy.

## Finding a skill

- **Catalog:** `skills-index.json` (or browse `skills/<category>/`)
- **Keyword:** `grep -ril "<topic>" skills --include=SKILL.md`
- **Semantic:** `tools/search_skills.sh "<what you're trying to do>"` — queries the
  local Qdrant collection `skills` (localhost:6357, machine-local)

## Maintenance

- **Refresh from sources:** pull the source clones (`~/.claude/claude-skills`,
  `~/.claude/mattpocock-skills`), then `python3 tools/consolidate.py` (rebuilds
  `skills/`, `skills-index.json`, `CONSOLIDATION.md`; source paths overridable via
  `SRC_CLAUDE_SKILLS` / `SRC_MP_SKILLS`).
- **Re-index:** `<agents-venv-python> tools/index_skills.py --recreate`
  (uses OpenAI `text-embedding-3-small`; key read from env or the Agents
  infrastructure `.env`).

## Skill format

agentskills.io convention — YAML frontmatter (`name`, `description` with trigger
phrases) + markdown body; bundled Python tools are stdlib-only (single documented
exception: `engineering/universal-scraping-architect`, deps declared in its
requirements.txt). Authoring guide: `docs/SKILL-AUTHORING-STANDARD.md`.
