build: ## Build the (local) package
	pip install -e .

install: ## Install the (local) package
	pip install -e .[dev]

.PHONY: tests
tests: ## Run tests
	pytest --junitxml=pytest.xml --cov-report=xml:coverage.xml --cov=src tests/

report:
	coverage report -m

# Thanks to Andreas Bauer
help: ## Show this help
	@grep -E '^[.a-zA-Z0-9_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'