# Project 01 specification: Azure end-to-end data platform

**Status:** Not started. **Domain:** e-commerce (fictional retailer "Tulip Trade").

## Scenario
Orders, customers and products live in an operational PostgreSQL database, payments
arrive from a payment-provider REST API, and suppliers drop product-catalogue CSV files.
Reporting is manual, duplicates exist, and there is no incremental loading.

## Scope
- Three source types: database extract, REST API, file drop.
- Medallion lakehouse on Delta Lake: Bronze (raw, immutable) -> Silver (typed, deduplicated,
  validated) -> Gold (analytics-ready: daily sales, customer 360, payment reconciliation).
- Incremental loading by watermark; deduplication by business key + latest version;
  late-arriving data handled by merge into Silver and re-derivation of affected Gold partitions;
  schema evolution (a new payments column appears mid-stream in the generated data).
- Validation with quarantine table and reasons.
- Authored Azure artefacts: Terraform (ADLS Gen2, Key Vault, Databricks workspace, Monitor),
  ADF pipeline/trigger JSON, Databricks job definition.

## Execution tiers (kept separate in the README)
| Tier | What runs | Evidence |
|---|---|---|
| Local | PySpark + Delta Lake in local mode, local filesystem standing in for ADLS Gen2, mock payments API, Docker Compose | Executed and tested |
| Authored | Terraform, ADF JSON, Databricks job spec | `terraform validate` / JSON schema checks only; not applied |
| Cloud | Real Azure deployment | Only if actually performed and recorded with date and cost |

A local filesystem and Azurite do not reproduce ADLS Gen2 hierarchical-namespace behaviour,
ADF triggers or Databricks autoscaling; the README states this.

## Acceptance criteria
1. Deterministic generator (seeded) emits duplicates, late records, one schema change, invalid rows.
2. Re-running the same batch leaves Silver/Gold row counts and checksums unchanged (idempotency test).
3. Late-arriving record updates the correct Silver row and Gold aggregate (test).
4. Schema evolution does not break the run and the new column is present in Silver (test).
5. Invalid rows land in quarantine with a reason code; counts reconcile: in = valid + quarantined + duplicates.
6. Unit tests for transforms run without Spark where possible; Spark integration tests run locally.
7. Benchmark: Bronze->Gold wall time and rows/s at three seeded volumes, per the benchmarking methodology.

## Out of scope
Real-time ingestion (Project 03), CDC (Project 04), BI dashboards.
