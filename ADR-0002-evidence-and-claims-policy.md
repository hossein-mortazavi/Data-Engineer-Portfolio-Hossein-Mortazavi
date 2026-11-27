# ADR-0002: Evidence and claims policy

- **Status:** Accepted
- **Date:** 2026-11-27

## Context

A portfolio is only useful if a reviewer can trust it. Overstated claims (untested
tools, invented benchmarks, implied production use) are the fastest way to lose that trust.

## Decision

Every capability, number and diagram in this repository carries one of these evidence
levels, and documentation must not imply a higher one.

| Level | Meaning |
|---|---|
| **Implemented and tested** | Code exists and automated tests were executed successfully (result recorded in the project README). |
| **Implemented** | Code exists and was run at least once, but lacks automated tests or CI coverage. |
| **Authored, not executed** | Written (e.g. Terraform, ADF JSON, compose files) but never applied or run. |
| **In progress / Planned** | Not complete; listed only so that scope is transparent. |

Additional rules:

- Datasets are synthetic and labelled as such. Business-impact statements are framed as
  scenario estimates and separated from measured engineering results.
- Benchmark numbers are committed only together with the script, the hardware and
  configuration used, and the raw output (see
  [`benchmarking-methodology.md`](../project-documentation/benchmarking-methodology.md)).
- Nothing is described as deployed to Azure unless it was deployed; local emulation is
  never described as equivalent to the managed service.
- No claim of production or customer usage.

## Consequences

Some tables will show "Planned" or "Authored, not executed" for a while. That is the
intended outcome: the repository reports its real state.
