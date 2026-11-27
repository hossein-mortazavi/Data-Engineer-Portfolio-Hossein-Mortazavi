# Contributing

This repository follows a lightweight, reviewable engineering workflow. Contributions and project changes should preserve reproducibility, testability, and evidence-based documentation.

## Setup

```bash
python3 -m venv .venv && source .venv/bin/activate
make install-dev
make check
```

## Rules

1. Follow [`docs/architecture/standards.md`](docs/architecture/standards.md).
2. One logical change per commit, imperative subject line (`Add watermark handling to Silver merge`).
3. Every behavioural change comes with a test. Pipelines must stay idempotent.
4. Never commit secrets; use `.env` (git-ignored) and document variables in `.env.example`.
5. Documentation must match the code. A README may only describe results that were produced
   by committed scripts (see [ADR-0002](docs/engineering-decisions/ADR-0002-evidence-and-claims-policy.md)).
6. Update [`skills-heatmap.md`](skills-heatmap.md) only after the capability is verified.

## Before opening a pull request

`make check` must pass, and any project you touched must pass its own tests.
