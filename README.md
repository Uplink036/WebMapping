# WebMapping

## Introduction

A comprehensive web mapping application that discovers and maps connections between websites. Starting from a given URL, it crawls outward to find linked websites. It can use plugins that can captures screenshots, detects bounding boxes, and it stores all such information in a Neo4j database. 

The application includes a web-based dashboard for monitoring crawling progress and viewing captured screenshots.

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

### Plugin Usage

The crawler supports plugins for additional functionality:

```python
from webmap import Crawler
from webmap.boundingbox import BoundingBoxCapture

# Initialize crawler with starting URL
crawler = Crawler("https://example.com")

# Add bounding box capture plugin
def capture_bounding_boxes(url: str) -> None:
    capture = BoundingBoxCapture()
    capture.capture_and_save(url)

crawler.add(capture_bounding_boxes)

# Start crawling with plugins
crawler.run()
```

### Web Dashboard

The application includes a web-based dashboard accessible at `http://localhost:8000` when running the main application. The dashboard provides real-time crawling statistics, crawler control, and screenshot viewing capabilities.

### Command Line Tools

The `tools/` directory contains utility scripts:

- `boundingbox.py`: Capture bounding box screenshots for a given URL
- `save_screenshot.py`: Retrieve and save screenshots from the database
- `clean_database.py`: Database maintenance utilities

See [main.py](./main.py) for a complete example.

### DevContainers

This project includes a devcontainer configuration for development in VS Code with Docker. This provides a consistent development environment with all dependencies pre-installed.

## Project Structure

```
src/webmap/
├── *.py                    # Main functionality
├── screenshot/             # Screenshot capture functionality
│   └── *.py
├── boundingbox/            # Bounding box detection and capture
│   └── *.py
└── database/               # Neo4j database integration
    └── *.py
```

## Contributions

Allowed to add anything you want, please follow resonable standards and the ones found in [docs](./docs/).

## License

**Author**: Uplink036

This project is licensed under the [MIT License](./LICENSE).