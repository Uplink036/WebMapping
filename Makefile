build: ## Build the (local) package
	pip install .

install: ## Install the (local) package
	pip install -e .[dev]

.PHONY: tests
tests: ## Run tests
	pytest --junitxml=pytest.xml --cov-report=xml:coverage.xml --cov=src tests/

report: ## Report coverage results
	coverage report -m

compose: ## Start the compose
	docker compose up

stop: ## Stop the compose
	docker compose down

lint: ## Lint source
	isort src/
	black src/
	mypy src/

clean: ## Clean the repo 
	rm -f pytest.xml
	rm -f coverage.xml
	rm -f .coverage
	rm -f .pytest_cache
	rm -f .hypothesis

# Thanks to Andreas Bauer
help: ## Show this help
	@grep -E '^[.a-zA-Z0-9_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'