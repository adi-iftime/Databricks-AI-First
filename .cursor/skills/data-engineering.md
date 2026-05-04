---
name: data-engineering
description: Pipelines, SQL, batch or stream processing, and warehouse-oriented data work.
type: skill
domain: data
---

# Skill: Data engineering

Reusable capability definition. **Not** tied to any single agent; routing is defined in orchestration rules.

## Technologies

- SQL and relational semantics
- Batch and stream processing stacks **as present in the repo** (e.g. Spark, notebooks, ELT tools)
- File and table formats common in the project (CSV, Parquet, etc.)

## Patterns

- Idempotent pipeline stages, reproducible transforms, schema evolution discipline
- Data quality checks (null rates, key uniqueness, referential checks) when appropriate
- Partitioning/time-window strategies for large datasets (when applicable)

## Domain knowledge

- Source vs curated vs serving layers (terminology may vary by org)
- PII handling, retention, and least-privilege access (follow org policies)
- Cost/latency tradeoffs for compute and storage

## Best practices

- Prefer explicit schemas/contracts where the codebase uses them
- Document assumptions about upstream data freshness and keys
- Avoid hardcoding secrets; use existing configuration mechanisms

## Separation (routing)

- **ML / predictive modeling** workstreams use `.cursor/skills/machine-learning.md`.
- **BI / reporting / KPI dashboards** use `.cursor/skills/business-intelligence.md`.
- This module covers **infrastructure and pipeline** style data engineering only.
