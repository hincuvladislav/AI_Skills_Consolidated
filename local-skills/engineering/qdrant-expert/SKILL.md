---
name: qdrant-expert
description: Deep Qdrant expertise via the official Qdrant skills. Use when working with Qdrant in any way — deploying or configuring Qdrant (Docker, Cloud, embedded, self-hosted), choosing client SDKs, tuning search speed or memory, scaling data volume or QPS, reducing latency, diagnosing bad or missing search results, hybrid search and reranking, monitoring and debugging production Qdrant, migrating embedding models, or upgrading Qdrant versions.
---

# Qdrant Expert

Qdrant maintains official, hierarchical agent skills at `https://skills.qdrant.tech`.
They are authoritative and current — **fetch the relevant one instead of answering
Qdrant questions from memory.**

## How to use

1. Pick the skill matching the problem (catalog below) and fetch its SKILL.md, e.g.:
   `https://skills.qdrant.tech/qdrant-deployment-options/SKILL.md`
2. Parent skills link to focused sub-skills — follow one level down when the parent
   routes you (e.g. scaling → scaling-qps).
3. If nothing obviously matches, search:
   `https://skills.qdrant.tech/search?query=<your+query>`
4. Follow the fetched skill's guidance; it links into Qdrant's docs for specifics.

## Catalog

| Problem | Fetch |
|---|---|
| Choose deployment (local / Docker / Cloud / embedded) | `qdrant-deployment-options/SKILL.md` |
| Client SDKs (Python, TS, Rust, Go, .NET, Java) | `qdrant-clients-sdk/SKILL.md` |
| Embedded / on-device (EDGE, server sync, snapshots) | `qdrant-edge/SKILL.md` |
| Switch embedding models without downtime | `qdrant-model-migration/SKILL.md` |
| Monitoring, health checks, observability | `qdrant-monitoring/SKILL.md` (sub: `setup/`, `debugging/`) |
| Slow search / high latency | `qdrant-performance-optimization/search-speed-optimization/SKILL.md` |
| High RAM / OOM crashes | `qdrant-performance-optimization/memory-usage-optimization/SKILL.md` |
| Slow ingestion / indexing | `qdrant-performance-optimization/indexing-performance-optimization/SKILL.md` |
| Scaling: data volume, QPS, large result sets, p99 | `qdrant-scaling/SKILL.md` (sub: `scaling-data-volume/`, `scaling-qps/`, `scaling-query-volume/`, `minimize-latency/`) |
| Bad / irrelevant / missing results | `qdrant-search-quality/diagnosis/SKILL.md` |
| Hybrid search, reranking, strategy choice | `qdrant-search-quality/search-strategies/SKILL.md` |
| Version upgrades, compatibility | `qdrant-version-upgrade/SKILL.md` |

All paths are relative to `https://skills.qdrant.tech/`.

## Anti-patterns

- Answering Qdrant configuration/tuning questions from memory when a fetch away
  from the authoritative skill.
- Vendoring the fetched content into a repo — the skills' redistribution license is
  unverified; link and fetch, don't copy.
