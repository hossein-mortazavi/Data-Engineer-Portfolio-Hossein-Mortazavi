# Phase 1 verification record

Date: 2026-11-27. Environment: sandbox with Python 3.12.3, GNU Make 4.3, OpenJDK 21,
1 CPU, 3.9 GB RAM, **no network access, no Docker, no Terraform**. Ruff, pytest, dbt,
PySpark, psql were not installed and could not be installed (package index unreachable).

## Executed and passed

| Check | Command | Result |
|---|---|---|
| Shared library unit tests | `python3 -m unittest discover -s tests -t .` | 24 tests, OK |
| Byte-compile all Python | `python3 -m compileall -q shared tests scripts` | OK |
| Secret scan (repository) | `python3 scripts/check_secrets.py` | 0 findings |
| Secret scan negative test | planted a hard-coded password in a temp copy | detected, exit 1 |
| Link check negative test | planted a broken link in a temp copy | detected, exit 1 |
| YAML parse | `yaml.safe_load` on CI workflow and compose file | OK |
| Shell syntax | `bash -n scripts/run_project_tests.sh` | OK |
| Makefile parse | `make -n check` | OK |

## Not executed (must be run on a machine with network and Docker)

| Item | Why not run | How to verify |
|---|---|---|
| Ruff lint and format check | Ruff not installable offline | `make install-dev && make lint` |
| pytest run (incl. coverage) | pytest not installable offline | `make test` |
| `docker compose config` / `up` for the root compose file | Docker unavailable | `cp .env.example .env && make up` |
| GitHub Actions workflow | Not pushed to GitHub | push and inspect the Actions tab |
| `scripts/run_project_tests.sh` end to end | No project test suites exist yet; needs network | runs automatically once projects have `tests/` |

The unit tests are written with `unittest` so that they run both under the standard
library runner (used here) and under pytest (used in CI).
