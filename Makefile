# Always able to run the following commands:
.PHONY: test build install

build: 
	python3 -m build

install:
	pip install -e .

test: 
	pytest