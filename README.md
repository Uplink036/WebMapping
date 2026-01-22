# WebMapping

## Introduction

A web mapping application that discovers and maps connections between websites. Starting from a given URL, it crawls outward to find linked websites and stores the relationships in a Neo4j graph database. Each website becomes a node in the graph, with edges representing the connections between them.

## Prerequisites

The project requires Python 3.12+ and all dependencies are managed through `pyproject.toml` and can be installed using the Makefile commands.

## Setup

### Database Setup

The application requires a Neo4j database. You can start one using Docker Compose:

```bash
make compose
```

This starts a Neo4j instance accessible at `http://localhost:7474` (web interface) and `bolt://localhost:7687` (database connection).

### Environment Configuration

Copy the example environment file and configure your database connection:

```bash
cp .env.example .env
```

Edit `.env` with your Neo4j credentials:
```
NEO4j_URI="neo4j://localhost:7687"
NEO4j_USERNAME="neo4j"
NEO4j_PASSWORD="password"
```

### Installation

Install the package in development mode with all dependencies:

```bash
make install
```

This installs the package with development dependencies including testing and linting tools.

## Usage

### Basic Usage

```python
from webmap import Crawler

# Initialize crawler with starting URL
crawler = Crawler("https://example.com")

# Start crawling
crawler.run()
```

See [main.py](./main.py) for a complete example.

### DevContainers

This project includes a devcontainer configuration for development in VS Code with Docker. This provides a consistent development environment with all dependencies pre-installed.

## Project Structure

```
src/webmap/
├── __init__.py          # Package initialization
├── crawler.py           # Main crawling logic
├── scraper.py          # HTML parsing and link extraction
├── url_handling.py     # URL processing utilities
└── database/           # Neo4j database integration
    ├── connection.py   # Database connection management
    ├── database.py     # Graph operations and stack management
    └── constants.py    # Database configuration constants
```

## License

**Author**: Uplink036

This project is licensed under the [MIT License](./LICENSE).