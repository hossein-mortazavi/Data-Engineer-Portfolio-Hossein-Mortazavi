.DEFAULT_GOAL := help
PYTHON ?= python3

.PHONY: help install-dev lint format test test-projects check-links check-secrets check up down clean

help: ## Show available targets
	@grep -E '^[a-zA-Z_-]+:.*?## ' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "} {printf "  %-16s %s\n", $$1, $$2}'

install-dev: ## Install repository-level developer tooling
	$(PYTHON) -m pip install -r requirements-dev.txt

lint: ## Static checks (ruff lint + format check)
	ruff check .
	ruff format --check .

format: ## Auto-format and fix lint issues
	ruff check --fix .
	ruff format .

test: ## Run repository-level unit tests (shared libraries)
	$(PYTHON) -m pytest

test-projects: ## Run every project's own test suite in isolated virtualenvs
	./scripts/run_project_tests.sh

check-links: ## Verify relative Markdown links resolve
	$(PYTHON) scripts/check_links.py

check-secrets: ## Scan for accidentally committed secrets
	$(PYTHON) scripts/check_secrets.py

check: lint test check-links check-secrets ## Everything CI runs for the repository foundation

up: ## Start the shared development PostgreSQL (requires .env)
	docker compose up -d --wait postgres

down: ## Stop shared development services
	docker compose down

clean: ## Remove caches and build artefacts
	find . -type d \( -name __pycache__ -o -name .pytest_cache -o -name .ruff_cache \) -prune -exec rm -rf {} +
	rm -rf htmlcov .coverage coverage.xml
