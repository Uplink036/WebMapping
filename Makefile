build: ## Build the (local) package
	python3 -m build

install: ## Install the (local) package
	pip install -r requirements.txt
	pip install -e .
	sudo apt install graphviz

.PHONY: test
test: ## Run tests
	pytest

cov: code-coverage ## Run tests with code coverage

code-coverage: ## Run tests with code coverage
	coverage run -m pytest

branch-coverage: ## Run tests with branch coverage
	coverage run -m --branch pytest

report: ## Generate coverage report
	coverage report -m --include="src/*"

# Thanks to Andreas Bauer
help: ## Show this help
	@grep -E '^[.a-zA-Z0-9_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'