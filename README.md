# Skills Library (consolidated)

One repo consolidating two agent-skills libraries for use by AI coding sessions on
this machine (and as a curation source for the OwnTeam platform).

| Source | Path | Skills | License |
|---|---|---|---|
| [alirezarezvani/claude-skills](https://github.com/alirezarezvani/claude-skills) (via fork `extendaretail-vladislav-hincu/claude-skills`, v2.9.0) | `vendor/claude-skills/` | ~355 | MIT © 2025 Alireza Rezvani |
| [mattpocock/skills](https://github.com/mattpocock/skills) | `vendor/mattpocock-skills/` | ~40 | MIT © 2026 Matt Pocock |

Total canonical `SKILL.md` files: **397** (platform-specific mirrors `.gemini/`,
`.hermes/`, `.vibe/`, `.codex/` were excluded at consolidation time).

## Layout

- `vendor/claude-skills/` — broad library: `engineering/`, `engineering-team/`,
  `product-team/`, `research/`, `project-management/`, `compliance-os/`,
  `marketing-skill/`, `c-level-advisor/`, … plus `agents/` (99 personas),
  `standards/`, `STORE.md` (index).
- `vendor/mattpocock-skills/skills/` — small composable engineering-workflow skills:
  `engineering/` (to-spec, to-tickets, implement, code-review, triage, wayfinder, tdd,
  diagnosing-bugs, domain-modeling, …), `productivity/`, `misc/`.
  Ignore `deprecated/` and `in-progress/`.
- `tools/` — indexing & semantic search against the local Qdrant instance
  (collection `skills`, Qdrant at `localhost:6357`).

## Finding a skill

- Keyword: `grep -ril "<topic>" vendor --include=SKILL.md`
- Semantic: `tools/search_skills.sh "<what you're trying to do>"`
- Human index: `vendor/claude-skills/STORE.md`, `vendor/mattpocock-skills/README.md`

## Skill format

agentskills.io convention: YAML frontmatter (`name`, `description` with trigger
phrases) + markdown body; optional `scripts/` (Python, stdlib-only), `references/`,
`assets/`.

## Licensing

Both sources are MIT; their license texts are retained at
`vendor/claude-skills/LICENSE` and `vendor/mattpocock-skills/LICENSE`. Keep those
notices when redistributing.

## Updating from sources

Source clones live at `~/.claude/claude-skills` (fork; `upstream` remote configured)
and `~/.claude/mattpocock-skills`. Pull them, re-run the rsync consolidation
(excluding `.git`, `.gemini`, `.hermes`, `.vibe`, `.codex`), then re-run
`tools/index_skills.py`.
