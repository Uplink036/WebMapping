# WebMapping

## Introduction

A project that is designed to map a part of the web. Meaning, given a URL, it will branch out from there and find more websites. After completion, it will show it's result in a graph, where a node represents a website and its edges the connection to others. 

In the future, there might be functionality to give the program n amounts of functions, which it will do once for each website. 

## How to Use
### Prerequisites

Current dependicdes are:
- Scraping
  - requests
  - html5lib
  - bs4
- Graphing
  - plotly
  - networkx
- Plotting
  - numpy
  - matplotlib
- Building
  - build

Most are needed, besides build. These can be installed using `pip install -r requirements.txt`

### Build
It can be built in two ways, which can be found in the [Makefile](./Makefile). Heres an excerpt from it. 

``` Makefile
build: ## Build the (local) package
	python3 -m build

install: ## Install the (local) package
	pip install -r requirements.txt
	pip install -e .
```

Usually you want to only use the `pip install -e .`, since then you can test the program and use in other scripts.

### Test

After the program has been built, i.e., `pip install -e .` and you have pytest and hypothesis installed. You can run `pytest`to test the program. 

### Run

Importing the WebMap by writting the following 
```Python
import webmap 

```

See the [main.py](./Main.py) script to see how it runs. 

### DevContainers

This project has a devcontainer, which you can use to get a working example up quicky, if you feel like it. Does require docker, and is helped by the vscode exstensions like [this](https://code.visualstudio.com/docs/devcontainers/containers).

## License

Author(s) - Uplink036 

This project uses [MIT license](./LICENSE).