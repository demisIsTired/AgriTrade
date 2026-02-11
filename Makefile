.PHONY: setup help lint format test test-cov docker-up docker-down clean

# Variables
PYTHON = python3
PIP = $(PYTHON) -m pip
DOCKER_COMPOSE ?= docker compose

help: ## Show this help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

setup: ## Install dependencies and setup pre-commit hooks
	$(PIP) install -r requirements.txt
	pre-commit install
	@echo "Setup complete. Pre-commit hooks installed."

## --- QA & LINTING ---

lint: ## Run Ruff linting and Mypy type checking
	ruff check . --fix
	mypy .

format: ## Auto-format code with Ruff
	ruff format .

test: ## Run unit and integration tests
	pytest

test-cov: ## Run tests with coverage enforcement
	pytest --cov=src --cov-report=term-missing --cov-fail-under=0

## --- INFRASTRUCTURE ---

docker-up: ## Start PostgreSQL and local dev environment
	$(DOCKER_COMPOSE) up -d

docker-down: ## Stop all containers
	$(DOCKER_COMPOSE) down

clean: ## Remove temporary files and python cache
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache .coverage .mypy_cache