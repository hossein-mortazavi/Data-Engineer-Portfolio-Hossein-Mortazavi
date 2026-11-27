# Azure end-to-end data platform

**Status: not started.** No code, results or claims exist for this project yet.

Medallion lakehouse (Bronze/Silver/Gold) with PySpark and Delta Lake, ADF-style orchestration, Terraform.

- Specification and acceptance criteria: [`project-01-spec.md`](../docs/project-documentation/project-01-spec.md)
- Standards this project must follow: [`standards.md`](../docs/architecture/standards.md)
- Evidence policy: [`ADR-0002`](../docs/engineering-decisions/ADR-0002-evidence-and-claims-policy.md)

This file will be replaced by the full case-study README
([template](../docs/project-documentation/README-template.md)) when the project is implemented and validated.

# Data warehouse and analytics engineering

**Status: not started.** No code, results or claims exist for this project yet.

PostgreSQL star schema modelled with dbt: SCD2, incremental models, SaaS metrics, tests and lineage.

- Specification and acceptance criteria: [`project-02-spec.md`](../docs/project-documentation/project-02-spec.md)
- Standards this project must follow: [`standards.md`](../docs/architecture/standards.md)
- Evidence policy: [`ADR-0002`](../docs/engineering-decisions/ADR-0002-evidence-and-claims-policy.md)

This file will be replaced by the full case-study README
([template](../docs/project-documentation/README-template.md)) when the project is implemented and validated.

# Real-time streaming platform

**Status: not started.** No code, results or claims exist for this project yet.

Kafka and Spark Structured Streaming with event-time windows, late/duplicate events and checkpoint recovery.

- Specification and acceptance criteria: [`project-03-spec.md`](../docs/project-documentation/project-03-spec.md)
- Standards this project must follow: [`standards.md`](../docs/architecture/standards.md)
- Evidence policy: [`ADR-0002`](../docs/engineering-decisions/ADR-0002-evidence-and-claims-policy.md)

This file will be replaced by the full case-study README
([template](../docs/project-documentation/README-template.md)) when the project is implemented and validated.


# Data integration and CDC platform

**Status: not started.** No code, results or claims exist for this project yet.

Debezium CDC and resilient API ingestion with idempotent sync, audit logging and reconciliation.

- Specification and acceptance criteria: [`project-04-spec.md`](../docs/project-documentation/project-04-spec.md)
- Standards this project must follow: [`standards.md`](../docs/architecture/standards.md)
- Evidence policy: [`ADR-0002`](../docs/engineering-decisions/ADR-0002-evidence-and-claims-policy.md)

This file will be replaced by the full case-study README
([template](../docs/project-documentation/README-template.md)) when the project is implemented and validated.


# Data quality and observability

**Status: not started.** No code, results or claims exist for this project yet.

Great Expectations and Airflow: detection, quarantine, scoring, reporting and alerting.

- Specification and acceptance criteria: [`project-05-spec.md`](../docs/project-documentation/project-05-spec.md)
- Standards this project must follow: [`standards.md`](../docs/architecture/standards.md)
- Evidence policy: [`ADR-0002`](../docs/engineering-decisions/ADR-0002-evidence-and-claims-policy.md)

This file will be replaced by the full case-study README
([template](../docs/project-documentation/README-template.md)) when the project is implemented and validated.


# Big data processing and optimisation

**Status: not started.** No code, results or claims exist for this project yet.

Repeatable Spark experiments on layout, partitioning, joins, shuffle and caching.

- Specification and acceptance criteria: [`project-06-spec.md`](../docs/project-documentation/project-06-spec.md)
- Standards this project must follow: [`standards.md`](../docs/architecture/standards.md)
- Evidence policy: [`ADR-0002`](../docs/engineering-decisions/ADR-0002-evidence-and-claims-policy.md)

This file will be replaced by the full case-study README
([template](../docs/project-documentation/README-template.md)) when the project is implemented and validated.




# Data dictionaries

Each project keeps its dictionary in this directory as `<project-slug>.md` once its
schemas are final (for example `01-azure-end-to-end-data-platform.md`).

## Required format

One section per table or topic:

```
### schema.table_name
Grain: one row per ...
Primary key: ...
Source: ... (system, endpoint or upstream model)
Refresh: batch / incremental / streaming, and expected frequency

| Column | Type | Nullable | Description | Validation |
|---|---|---|---|---|
```

Rules: describe business meaning, not just the type; name the validation that enforces
each constraint; mark every dataset as synthetic. Dictionaries are checked against the
schemas under `data/schemas/` before a project is marked complete.
