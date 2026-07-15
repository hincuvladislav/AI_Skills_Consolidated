# Consolidation log

Units kept: **316** · decisions below. Rules: R1 byte-identical dedup · R2 stale forks of original-author skills dropped · R3 same-name different-skill kept in separate categories · R4 composite units kept intact (sub-skill name overlap is not a conflict).

Sources: alirezarezvani/claude-skills v2.9.0 (MIT) · mattpocock/skills (MIT). mattpocock `deprecated/`, `in-progress/`, `personal/` excluded by policy.

## Decisions

- SKIP `claude-skills/productivity/handoff` — expanded fork of mattpocock's `handoff`; original author's current version kept as `productivity/handoff` (R2)
- KEEP BOTH `research/research` and `workflow/research` — same name, different skills (R3)
- SKIP `claude-skills/c-level-advisor/skills/arquiteto-de-empresa` — byte-identical to kept `c-level/arquiteto-de-empresa` (R1)
- SKIP `claude-skills/c-level-advisor/skills/chief-ai-officer-advisor` — byte-identical to kept `c-level/chief-ai-officer-advisor` (R1)
- SKIP `claude-skills/c-level-advisor/skills/chief-customer-officer-advisor` — byte-identical to kept `c-level/chief-customer-officer-advisor` (R1)
- SKIP `claude-skills/c-level-advisor/skills/chief-data-officer-advisor` — byte-identical to kept `c-level/chief-data-officer-advisor` (R1)
- SKIP `claude-skills/c-level-advisor/skills/general-counsel-advisor` — byte-identical to kept `c-level/general-counsel-advisor` (R1)
- SKIP `claude-skills/c-level-advisor/vpe-advisor` — name collision with already-kept `c-level/vpe-advisor` (first-kept wins; review manually)
- SKIP `claude-skills/engineering/grill-me` — stale fork of mattpocock's `grill-me` (R2); kept the original author's current version
- SKIP `claude-skills/engineering/grill-with-docs` — stale fork of mattpocock's `grill-with-docs` (R2); kept the original author's current version
- SKIP `claude-skills/engineering/handoff` — expanded fork of mattpocock's `handoff`; original author's current version kept as `productivity/handoff` (R2)
- SKIP `claude-skills/engineering/skills/chaos-engineering` — byte-identical to kept `engineering/chaos-engineering` (R1)
- SKIP `claude-skills/engineering/skills/feature-flags-architect` — byte-identical to kept `engineering/feature-flags-architect` (R1)
- SKIP `claude-skills/engineering/skills/kubernetes-operator` — byte-identical to kept `engineering/kubernetes-operator` (R1)
- SKIP `claude-skills/engineering/slo-architect` — name collision with already-kept `engineering/slo-architect` (first-kept wins; review manually)
- SKIP `claude-skills/productivity/handoff` — name collision with already-kept `productivity/handoff` (first-kept wins; review manually)
