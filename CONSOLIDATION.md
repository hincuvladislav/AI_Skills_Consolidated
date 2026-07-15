# Consolidation log

Units kept: **334** · decisions below. Rules: R1 byte-identical dedup · R2 stale/expanded forks dropped in favor of the original author's current version · R3 same-name different-skill kept in separate categories · R4 composite units kept intact (sub-skill name overlap is not a conflict).

Sources (pinned in `sources.lock.json`): alirezarezvani/claude-skills (MIT) · mattpocock/skills (MIT) · obra/superpowers (MIT) · anthropics/skills (Apache-2.0 picks only — the source-available docx/pdf/pptx/xlsx skills are never ingested). mattpocock `deprecated/`, `in-progress/`, `personal/` excluded by policy.

## Decisions

- KEEP BOTH `research/research` and `workflow/research` — same name, different skills (R3)
- SKIP `claude-skills/c-level-advisor/skills/arquiteto-de-empresa` — byte-identical to kept `c-level/arquiteto-de-empresa` (R1)
- SKIP `claude-skills/c-level-advisor/skills/chief-ai-officer-advisor` — byte-identical to kept `c-level/chief-ai-officer-advisor` (R1)
- SKIP `claude-skills/c-level-advisor/skills/chief-customer-officer-advisor` — byte-identical to kept `c-level/chief-customer-officer-advisor` (R1)
- SKIP `claude-skills/c-level-advisor/skills/chief-data-officer-advisor` — byte-identical to kept `c-level/chief-data-officer-advisor` (R1)
- SKIP `claude-skills/c-level-advisor/skills/general-counsel-advisor` — byte-identical to kept `c-level/general-counsel-advisor` (R1)
- SKIP `claude-skills/c-level-advisor/vpe-advisor` — byte-identical to kept `c-level/vpe-advisor` (R1)
- SKIP `claude-skills/engineering/grill-me` — stale fork of mattpocock's `grill-me` (R2); kept the original author's current version
- SKIP `claude-skills/engineering/grill-with-docs` — stale fork of mattpocock's `grill-with-docs` (R2); kept the original author's current version
- SKIP `claude-skills/engineering/handoff` — expanded fork of mattpocock's `handoff`; original author's current version kept (R2)
- SKIP `claude-skills/engineering/skills/chaos-engineering` — byte-identical to kept `engineering/chaos-engineering` (R1)
- SKIP `claude-skills/engineering/skills/feature-flags-architect` — byte-identical to kept `engineering/feature-flags-architect` (R1)
- SKIP `claude-skills/engineering/skills/kubernetes-operator` — byte-identical to kept `engineering/kubernetes-operator` (R1)
- SKIP `claude-skills/engineering/skills/skill-tester/assets/sample-skill` — upstream test fixture, not a skill
- SKIP `claude-skills/engineering/slo-architect` — byte-identical to kept `engineering/slo-architect` (R1)
- SKIP `claude-skills/productivity/handoff` — expanded fork of mattpocock's `handoff`; original author's current version kept (R2)
