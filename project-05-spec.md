# Project 05 specification: data quality and observability

**Status:** Not started. **Domain:** financial services (loan applications, repayments, external credit-bureau files).

## Scenario
Internal and external feeds arrive with missing records, duplicates and silent schema changes,
producing unreliable regulatory and management reports.

## Scope
- Great Expectations suites plus custom SQL/Pandas checks: schema, nulls, uniqueness, referential
  integrity, business rules, freshness, distribution drift.
- Anomaly detection on volume and distribution (statistical baseline; method documented with its limits).
- Data quality score per dataset and run, stored in PostgreSQL; HTML validation reports.
- Airflow DAG: ingest -> validate -> quarantine failing rows -> publish good data -> notify on failure.
- Notification via a configurable webhook/email sink (a local mock sink is used in tests).

## Acceptance criteria
1. A seeded fault injector creates each class of defect; every injected defect is detected,
   isolated in quarantine with a reason, and reported (detection-rate table, measured).
2. Clean data produces a passing run with no quarantined rows (false-positive check).
3. A schema change fails the run before publication.
4. DAG parses in CI and a full DAG run is executed locally with the results recorded.

## Out of scope
Commercial observability platforms; ML-based anomaly models beyond the documented statistical approach.
