# Consolidation log

Units kept: **334** · decisions below. Rules: R1 byte-identical dedup · R2 stale/expanded forks dropped in favor of the original author's current version · R3 same-name different-skill kept in separate categories · R4 composite units kept intact (sub-skill name overlap is not a conflict).

Input ids (s1..s4, local) are resolved in `MAINTAINERS.md` (maintainers-only provenance file). One input's `deprecated/`, `in-progress/`, `personal/` dirs are excluded by policy.

## Decisions

- KEEP BOTH `research/research` and `workflow/research` — same name, different skills (R3)
- RENAME `s2/skills/engineering/ask-matt` -> `workflow/which-skill` — neutral naming policy
- RENAME `s2/skills/engineering/setup-matt-pocock-skills` -> `workflow/setup-workflow-skills` — neutral naming policy
- SKIP `s1/c-level-advisor/skills/arquiteto-de-empresa` — byte-identical to kept `c-level/arquiteto-de-empresa` (R1)
- SKIP `s1/c-level-advisor/skills/chief-ai-officer-advisor` — byte-identical to kept `c-level/chief-ai-officer-advisor` (R1)
- SKIP `s1/c-level-advisor/skills/chief-customer-officer-advisor` — byte-identical to kept `c-level/chief-customer-officer-advisor` (R1)
- SKIP `s1/c-level-advisor/skills/chief-data-officer-advisor` — byte-identical to kept `c-level/chief-data-officer-advisor` (R1)
- SKIP `s1/c-level-advisor/skills/general-counsel-advisor` — byte-identical to kept `c-level/general-counsel-advisor` (R1)
- SKIP `s1/c-level-advisor/vpe-advisor` — byte-identical to kept `c-level/vpe-advisor` (R1)
- SKIP `s1/engineering/grill-me` — stale/expanded fork; the original author's current version is kept (R2)
- SKIP `s1/engineering/grill-with-docs` — stale/expanded fork; the original author's current version is kept (R2)
- SKIP `s1/engineering/handoff` — stale/expanded fork; the original author's current version is kept (R2)
- SKIP `s1/engineering/skills/chaos-engineering` — byte-identical to kept `engineering/chaos-engineering` (R1)
- SKIP `s1/engineering/skills/feature-flags-architect` — byte-identical to kept `engineering/feature-flags-architect` (R1)
- SKIP `s1/engineering/skills/kubernetes-operator` — byte-identical to kept `engineering/kubernetes-operator` (R1)
- SKIP `s1/engineering/skills/skill-tester/assets/sample-skill` — upstream test fixture, not a skill
- SKIP `s1/engineering/slo-architect` — byte-identical to kept `engineering/slo-architect` (R1)
- SKIP `s1/productivity/handoff` — stale/expanded fork; the original author's current version is kept (R2)
- SKIP `s3/skills/using-superpowers` — meta-skill tied to its home plugin, no value standalone
