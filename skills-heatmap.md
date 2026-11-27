# Skills heatmap

Maps technologies to projects. A cell is only upgraded when the capability has been built
**and verified**; the evidence levels are defined in
[ADR-0002](docs/engineering-decisions/ADR-0002-evidence-and-claims-policy.md).

Legend: **IT** implemented and tested, **I** implemented, **A** authored not executed,
**IP** in progress, **P** planned, **-** not used in that project.

## Foundation (Phase 1)

| Capability | Status | Evidence |
|---|---|---|
| Python shared library (config, structured logging, retry/backoff, errors) | IT | 24 unit tests run with `unittest`; also written to run under pytest (see phase-1 verification) |
| Repository scripts (link check, secret scan, project test runner) | I | Link check and secret scan executed locally; project test runner syntax-checked only |
| GitHub Actions CI | A | Workflow YAML parses; never executed on GitHub |
| Docker Compose (shared PostgreSQL) | A | YAML parses; Docker was unavailable, so never run |
| Ruff / pytest configuration | A | Configured; Ruff and pytest were not installable in the authoring environment |

## Technologies by project

| Technology | 01 | 02 | 03 | 04 | 05 | 06 |
|---|---|---|---|---|---|---|
| Python | P | P | P | P | P | P |
| SQL / PostgreSQL | P | P | P | P | P | - |
| PySpark / Spark | P | - | P | - | - | P |
| Delta Lake | P | - | - | - | - | P |
| Parquet | P | - | - | - | - | P |
| Azure Data Lake Storage Gen2 | P (local stand-in) | - | - | - | - | - |
| Azure Data Factory | P (authored) | - | - | - | - | - |
| Azure Databricks | P (authored) | - | - | - | - | - |
| Azure Key Vault / Monitor | P (authored) | - | - | - | - | - |
| Terraform | P (authored) | - | - | - | - | - |
| dbt | - | P | - | - | - | - |
| Metabase | - | P | - | - | - | - |
| Apache Kafka | - | - | P | P | - | - |
| Spark Structured Streaming | - | - | P | - | - | - |
| Debezium | - | - | - | P | - | - |
| REST API ingestion | P | - | - | P | - | - |
| Great Expectations | - | - | - | - | P | - |
| Apache Airflow | - | - | - | - | P | - |
| Pandas | - | - | - | - | P | - |
| Docker / Compose | P | P | P | P | P | P |
| pytest / Ruff / CI | P | P | P | P | P | P |
