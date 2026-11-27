#!/usr/bin/env bash
# Run the test suite of every numbered project that has a tests/ directory.
# Each project installs its own requirements.txt into an isolated virtualenv so that
# dependency conflicts between projects (e.g. Spark vs Airflow) cannot hide.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
status=0
found=0

for project in "$ROOT"/[0-9][0-9]-*/; do
  [ -d "${project}tests" ] || continue
  found=$((found + 1))
  name="$(basename "$project")"
  echo "=== ${name} ==="
  venv="$(mktemp -d)/venv"
  python3 -m venv "$venv"
  if [ -f "${project}requirements.txt" ]; then
    "$venv/bin/pip" install --quiet -r "${project}requirements.txt"
  fi
  "$venv/bin/pip" install --quiet -r "$ROOT/requirements-dev.txt"
  (cd "$project" && PYTHONPATH="$ROOT:$project" "$venv/bin/python" -m pytest tests -q) || status=1
done

if [ "$found" -eq 0 ]; then
  echo "No project test suites found yet."
fi
exit "$status"
