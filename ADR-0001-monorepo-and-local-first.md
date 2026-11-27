# ADR-0001: One repository, local-first execution

- **Status:** Accepted
- **Date:** 2026-11-27

## Context

The portfolio contains six projects that must be reviewable by recruiters without a
cloud subscription, yet should reflect production practices (Azure, Kafka, Spark).

## Decision

1. Keep all projects in one repository with shared tooling (lint, CI, secret scan) and a
   small `shared/` library for cross-cutting concerns only.
2. Every project runs locally (Docker Compose or local Spark) on synthetic data.
3. Cloud-only services (Azure Data Factory, Databricks, Key Vault, Monitor) are covered
   by two things: authored infrastructure/pipeline definitions, and local stand-ins for
   the data-plane behaviour. The two are always labelled separately.
4. Each project keeps its own `requirements.txt` and `docker-compose.yml` so it can be
   run in isolation and does not drag unrelated dependencies (e.g. Spark vs Airflow).

## Consequences

- Recruiters can reproduce results with `docker compose up` and `make`.
- The Azure project cannot demonstrate managed-service behaviour (autoscaling, ADF
  triggers, Unity Catalog) unless it is actually deployed; the README says so.
- CI has to cope with heterogeneous toolchains, hence per-project virtualenvs.
