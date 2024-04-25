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
	coverage report -m --include="src/*"

branch-coverage:
	coverage run -m --branch pytest
	coverage report -m --include="src/*"