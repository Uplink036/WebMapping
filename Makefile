# Always able to run the following commands:
.PHONY: test build install cov code-coverage branch-coverage

build: 
	python3 -m build

install:
	pip install -e .

test: 
	pytest

cov: code-coverage

code-coverage:
	coverage run -m pytest

branch-coverage:
	coverage run -m --branch pytest

report: 
	coverage report -m --include="src/*"

# Thanks to Andreas Bauer
help: ## Show this help
	@grep -E '^[.a-zA-Z0-9_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'