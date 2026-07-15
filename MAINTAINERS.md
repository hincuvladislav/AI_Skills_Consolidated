# MAINTAINERS — provenance & source management

> Maintainers-only. This is the **single place** that names the library's input
> repositories. Everywhere else (CONSOLIDATION.md, skills-index.json, LICENSES/
> filenames, tools) inputs are referenced by opaque ids.

## Source ids

| id | Repository | License | What we ingest |
|---|---|---|---|
| `s1` | github.com/alirezarezvani/claude-skills (via fork extendaretail-vladislav-hincu/claude-skills) | MIT © 2025 Alireza Rezvani | broad library — all category dirs mapped in `tools/consolidate.py` |
| `s2` | github.com/mattpocock/skills | MIT © 2026 Matt Pocock | `skills/engineering|productivity|misc` → `workflow/`, `productivity/`, `misc/`; `deprecated/`, `in-progress/`, `personal/` excluded. **Wins dedup ties as original author** (s1 carries stale forks of several of these skills) |
| `s3` | github.com/obra/superpowers | MIT | all 14 skills → `methodology/` |
| `s4` | github.com/anthropics/skills | Apache-2.0 **per-skill** | ONLY skill-creator, mcp-builder, webapp-testing, claude-api, frontend-design → `engineering/`. The docx/pdf/pptx/xlsx skills are **source-available, not open source → never ingest** |
| `local` | `local-skills/` in this repo | repo license | library-authored skills; survive rebuilds |

License notices: `LICENSES/LICENSE-s1..s3` (repo-level) and per-skill `LICENSE.txt`
inside each s4 skill. **These must remain in any redistribution.**

Local clones (override via `SRC_S1..SRC_S4` env):
`~/.claude/claude-skills` (s1, fork with `upstream` remote configured) ·
`~/.claude/mattpocock-skills` (s2) · `~/.claude/superpowers` (s3) ·
`~/.claude/anthropic-skills` (s4).

## Pinned commits

Regenerated automatically by `tools/consolidate.py` on every rebuild:

<!-- PINS:BEGIN -->
```json
{
  "s1": {
    "origin": "https://github.com/extendaretail-vladislav-hincu/claude-skills.git",
    "commit": "84dc5a4f6ab93df5195805010572d7d0f874dadb"
  },
  "s2": {
    "origin": "https://github.com/mattpocock/skills.git",
    "commit": "e9fcdf95b402d360f90f1db8d776d5dd450f9234"
  },
  "s3": {
    "origin": "https://github.com/obra/superpowers.git",
    "commit": "d884ae04edebef577e82ff7c4e143debd0bbec99"
  },
  "s4": {
    "origin": "https://github.com/anthropics/skills.git",
    "commit": "9d2f1ae187231d8199c64b5b762e1bdf2244733d"
  }
}
```
<!-- PINS:END -->

## Refresh workflow

1. `git pull` each source clone; **review the upstream diff** before consolidating
   (supply-chain policy — see docs/ECOSYSTEM.md §curation).
2. `python3 tools/consolidate.py` — rebuilds `skills/`, `skills-index.json`,
   `CONSOLIDATION.md`, `LICENSES/`, and the pins block above.
3. `python3 tools/validate_skills.py --quiet` — investigate any new errors.
4. Re-index: `<venv-python> tools/index_skills.py --recreate`.
5. Commit; mention the new pins in the message body if sources moved.

## Evaluated, not ingested (candidates & rejections)

- **vercel-labs/agent-skills** — 3 of the global top-10 most-installed skills, but
  **no license file** → cannot redistribute. Revisit if licensed.
- **Qdrant official skills** (skills.qdrant.tech, ~20 hierarchical skills:
  deployment, scaling, monitoring, performance, search quality, migrations) —
  high quality, but **license/source repo unverified** (checked 2026-07-14; only
  unofficial mirrors on GitHub) → linked, not vendored:
  `local-skills/engineering/qdrant-expert` routes agents to fetch them at need.
  Revisit if Qdrant publishes a licensed repo.
- Vendor-official stacks, add on demand: cloudflare/skills (Apache-2.0),
  supabase/agent-skills (MIT), expo/skills (MIT), Kotlin/kotlin-agent-skills
  (Apache-2.0), antfu/skills (MIT), K-Dense-AI/scientific-agent-skills (MIT).
- **sickn33/agentic-awesome-skills** (1,900+ claimed) — unaudited mega-library;
  contradicts curation policy. Rejected.
- Discovery feed: VoltAgent/awesome-agent-skills.

## Known upstream non-conformances (kept as-is)

- `engineering/playwright-pro/skills/pw` — internal dir intentionally short-named.
- `research/litreview` — description 1161 chars (>1024 spec limit).
