# AI Skills Consolidated

A curated library of **334 agent skills** across **16 domains** — reusable expertise
packages that give AI coding agents (Claude Code, Codex, Cursor, Gemini CLI, and any
other agent that reads `SKILL.md` files) structured workflows, domain knowledge, and
executable tools they don't have out of the box.

Every skill follows the open [agentskills.io](https://agentskills.io/specification)
convention:

```
skill-name/
├── SKILL.md        # YAML frontmatter (name + description) + instructions, ≤500 lines
├── scripts/        # executable CLI tools (Python, stdlib-only)
├── references/     # deeper knowledge, loaded only when needed
└── assets/         # templates and samples
```

**223 of the 334 skills ship executable tools** — linters, scorers, generators — all
plain Python with zero external dependencies, so they run anywhere Python runs.

---

## What's inside

| Category | Skills | What it covers |
|---|---|---|
| `engineering/` | 107 | code review, API design, testing, security, architecture, DevOps, observability, anti-hallucination coding disciplines |
| `marketing/` | 49 | campaigns, SEO/AEO, analytics, content, brand |
| `c-level/` | 36 | CEO/CFO/CTO/CISO/CMO-level advisory personas |
| `business/` | 20 | growth, operations, commercial |
| `ra-qm/` | 19 | regulatory affairs & quality management |
| `product/` | 17 | PRDs, prioritization, product-owner toolkits |
| `workflow/` | 17 | the delivery loop: spec → tickets → implement → review → triage → debug |
| `methodology/` | 14 | engineering discipline: TDD, systematic debugging, plan writing & execution, verification before completion |
| `productivity/` | 10 | capture, teach, handoff, grilling sessions |
| `research/` | 9 | deep research, literature review, competitive intel |
| `project-management/` | 9 | planning, estimation, status reporting |
| `compliance/` | 9 | AI-act readiness, audits, governance |
| `research-ops/` | 5 | clinical/market/product research operations |
| `documents/` | 5 | Markdown/HTML document production |
| `finance/` | 4 | budgeting, investment analysis |
| `misc/` | 4 | odds and ends (git guardrails, pre-commit setup, …) |

Plus, outside `skills/`:

- **`agents/`** — 99 role personas (backend engineer, senior architect, adversarial
  reviewer, …) that pair with skills
- **`commands/`** — slash-command definitions for Claude Code
- **`standards/`** — process standards (communication, quality, git, documentation, security)
- **`templates/`**, **`docs/`** — authoring templates, the skill-authoring standard, and
  ecosystem/maintenance notes
- **`skills-index.json`** — machine-readable catalog of every skill (name, category,
  path, description, tooling flags)

---

## Quick start

### 1. Get the repo

```bash
git clone https://github.com/hincuvladislav/AI_Skills_Consolidated.git
cd AI_Skills_Consolidated
```

### 2. Install skills into your agent

> **⚠ Install per-domain, not everything.** Agents cap how many skill descriptions
> they can hold (Claude Code caps the listing at ~1% of context) — past ~20-25
> installed skills, the least-used ones silently stop auto-triggering. Pick the
> categories you actually work in; use the search below for everything else.

**Claude Code** — copy the skill dirs you want into a skills location:

```bash
# per-project
mkdir -p .claude/skills
cp -R skills/methodology/systematic-debugging .claude/skills/

# or user-wide
cp -R skills/workflow/code-review ~/.claude/skills/
```

**Codex / Cursor / Copilot / Gemini CLI / Goose / OpenCode** — these all honor the
vendor-neutral path:

```bash
mkdir -p ~/.agents/skills          # or $REPO_ROOT/.agents/skills per-project
cp -R skills/engineering/api-design-reviewer ~/.agents/skills/
```

**Any other agent** — a skill is just a folder; point your agent at the skill's
`SKILL.md` (paste it into context if the agent has no skill mechanism) and its
`scripts/` tools run standalone:

```bash
python3 skills/engineering/api-design-reviewer/scripts/api_linter.py --help
```

### 3. Use a skill

Skills auto-trigger when your request matches their description ("review this PR",
"debug this", "write a spec"). You can also invoke explicitly — e.g. in Claude Code
mention the skill by name, or run its bundled tools directly from the shell.

---

## Finding the right skill

Three ways, fastest first:

1. **Browse the catalog** — `skills-index.json` has every skill's name, category and
   description; or just explore `skills/<category>/`.
2. **Keyword search:**
   ```bash
   grep -ril "merge conflict" skills --include=SKILL.md
   ```
3. **Semantic search** (optional, requires a local [Qdrant](https://qdrant.tech)
   instance + an OpenAI API key for embeddings):
   ```bash
   # one-time: build the vector index
   python3 tools/index_skills.py --recreate
   # then search by intent, not keywords
   tools/search_skills.sh "verify my change actually works before finishing"
   ```
   Configure via env: `QDRANT_HOST` / `QDRANT_PORT` (default `localhost:6357`),
   `OPENAI_API_KEY`. Requires `pip install qdrant-client openai python-dotenv`.

---

## Recommended starter sets

| If you are… | Install these |
|---|---|
| A developer using an AI agent daily | `workflow/` (all 17) — the full delivery loop: `to-spec`, `to-tickets`, `implement`, `code-review`, `triage`, `diagnosing-bugs`, `wayfinder` |
| Focused on code quality | `methodology/test-driven-development`, `methodology/systematic-debugging`, `methodology/verification-before-completion`, `engineering/adversarial-reviewer`, `engineering/dependency-auditor` |
| Building APIs | `engineering/api-design-reviewer`, `engineering/api-test-suite-builder`, `engineering/strict-api` |
| Shipping to production | `engineering/ship-gate`, `engineering/slo-architect`, `engineering/observability-designer`, `engineering/security-guidance` |
| Writing your own skills | `engineering/skill-creator` (includes an eval harness), `engineering/write-a-skill`, `methodology/writing-skills`, plus `docs/SKILL-AUTHORING-STANDARD.md` |

---

## Tools

| Tool | Purpose |
|---|---|
| `tools/validate_skills.py [--strict] [--quiet]` | Lint every skill against the agentskills.io spec (name==dir, name format, description ≤1024 chars, body <500 lines / <5k tokens, frontmatter fields) |
| `tools/index_skills.py [--recreate]` | Build/refresh the semantic-search index (Qdrant collection `skills`) |
| `tools/search_skills.sh "<query>" [n]` | Semantic search over all skills |
| `tools/consolidate.py` | Maintainer tool: rebuilds `skills/`, `skills-index.json` and the decision log from configured sources |

---

## Repository structure

```
skills/<category>/<skill>/    # 334 skill units — the library itself
agents/                       # 99 role personas
commands/                     # slash-command definitions
standards/                    # process standards
templates/                    # authoring templates
docs/                         # authoring standard, conventions, ecosystem notes
tools/                        # validate / index / search / consolidate
skills-index.json             # machine-readable catalog
sources.lock.json             # provenance pinning (maintainers)
CONSOLIDATION.md              # curation decision log (maintainers)
LICENSES/                     # third-party license notices — keep when redistributing
```

## Conventions & guarantees

- **One skill = one folder.** Nothing outside a skill's folder is needed to use it
  (except the optional shared search tooling).
- **Composite skills** (7 of them, e.g. `engineering/playwright-pro`) bundle several
  sub-skills under one unit — install the whole folder.
- **Scripts are stdlib-only Python** (one documented exception:
  `engineering/universal-scraping-architect` declares its deps in its own
  requirements.txt).
- **Descriptions are the discovery surface** — every skill states what it does and
  when to trigger it in frontmatter, per the
  [authoring standard](docs/SKILL-AUTHORING-STANDARD.md).
- **Provenance is pinned** — the library is rebuilt only from reviewed, SHA-pinned
  inputs; no open contribution pipeline, no unreviewed skill ever lands here.

## Licensing

Individual skills retain their original licenses (MIT / Apache-2.0). The notices in
`LICENSES/` and per-skill `LICENSE.txt` files must be preserved when redistributing.

