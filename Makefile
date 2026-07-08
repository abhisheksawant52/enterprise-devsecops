.DEFAULT_GOAL := help
.PHONY: help install lint format test build clean run \
	tf-fmt tf-validate helm-lint docker-build

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-14s\033[0m %s\n", $$1, $$2}'

install: ## Install package with dev dependencies
	python -m pip install --upgrade pip
	pip install -e ".[dev]"

lint: ## Run ruff and black in check mode
	ruff check src tests
	black --check src tests

format: ## Auto-format the codebase
	ruff check --fix src tests
	black src tests

test: ## Run the test suite
	pytest

build: ## Build distribution artifacts
	python -m pip install --upgrade build
	python -m build

run: ## Run the platform service locally
	uvicorn enterprise_devsecops.service:app --reload --port 8080

docker-build: ## Build the service container image
	docker build -t enterprise-devsecops:local .

tf-fmt: ## Check Terraform formatting
	terraform -chdir=terraform fmt -check -recursive

tf-validate: ## Initialize (no backend) and validate Terraform
	terraform -chdir=terraform init -backend=false -input=false
	terraform -chdir=terraform validate

helm-lint: ## Lint the Helm chart
	helm lint helm

clean: ## Remove build and cache artifacts
	rm -rf build dist *.egg-info src/*.egg-info .pytest_cache .ruff_cache
	find . -type d -name __pycache__ -prune -exec rm -rf {} +
