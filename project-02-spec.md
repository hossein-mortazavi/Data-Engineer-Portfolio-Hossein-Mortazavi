# Project 02 specification: SaaS data warehouse and analytics engineering

**Status:** Not started. **Domain:** B2B SaaS subscriptions (fictional "Meridian Analytics").

## Scenario
Finance, product and customer success compute MRR, churn and retention differently from the
same operational tables. A single governed warehouse must produce one definition of each metric.

## Scope
- PostgreSQL warehouse; dbt layers: `staging` -> `intermediate` -> `marts`.
- Star schema: facts (subscription periods, invoices/payments, product usage events),
  dimensions (customer, plan, date); SCD Type 2 on customer and plan via dbt snapshots.
- Incremental dbt models for the large usage fact.
- Metrics: MRR, ARR, logo churn, revenue churn (gross and net), customer retention, LTV,
  MAU, monthly cohort retention. Each metric has a written definition and a SQL implementation.
- dbt tests (unique, not_null, relationships, accepted_values, custom metric-reconciliation
  tests), generated docs and lineage graph, query-plan based optimisation notes (indexes,
  partial indexes, pre-aggregation) with before/after `EXPLAIN ANALYZE`.
- Metabase over the marts (Power BI is not used: it cannot run in Docker/Linux).

## Acceptance criteria
1. `docker compose up` + `make build` loads seeded synthetic data and runs `dbt build` green.
2. A hand-computed fixture (small dataset with known answers) matches MRR/churn/retention output.
3. SCD2 test: changing a plan price creates a new dimension row with correct validity ranges.
4. Incremental model test: second run processes only new rows and yields the same result as a full refresh.
5. Optimisation claims backed by committed `EXPLAIN ANALYZE` output.
6. README explains, with examples, how the warehouse removes conflicting metric definitions.

## Out of scope
Streaming and CDC ingestion; ML-based churn prediction.
