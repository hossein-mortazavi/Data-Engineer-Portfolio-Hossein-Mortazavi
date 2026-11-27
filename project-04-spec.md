# Project 04 specification: data integration and CDC platform

**Status:** Not started. **Domain:** telecommunications (CRM database, billing database, partner usage API).

## Scenario
Customer, subscription and usage data is replicated between operational systems by nightly
full extracts that are slow and miss intra-day changes.

## Scope
- Sources: two PostgreSQL databases (CRM, billing) and a mock paginated, rate-limited REST API.
- CDC with Debezium -> Kafka -> Python sink applying changes idempotently to a target PostgreSQL.
- API ingestion client: pagination, rate-limit handling (HTTP 429 / Retry-After), retries with
  exponential backoff (reusing `shared.utilities.retry`), incremental cursors.
- Audit log of every applied batch; reconciliation job comparing source and target (counts and
  row-level checksums).
- Schema change handling (added column) demonstrated end to end.

## Acceptance criteria
1. Inserts, updates and deletes in the sources appear in the target; reconciliation reports zero diffs.
2. Replaying the same change events twice leaves the target unchanged (idempotency test).
3. API client survives injected 429/5xx responses and resumes from its cursor after a crash.
4. Measured comparison, same data and hardware: rows and bytes read by CDC vs full refresh across
   several change rates (1%, 5%, 20%); raw results committed.

## Out of scope
Multi-region replication, Kafka Connect cluster operations.
