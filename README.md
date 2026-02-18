# WebMapping

## Introduction

A comprehensive web mapping application that discovers and maps connections between websites. Starting from a given URL, it crawls outward to find linked websites. It can use plugins that can captures screenshots, detects bounding boxes, and it stores all such information in a Neo4j database. 

The application includes a web-based dashboard for monitoring crawling progress and viewing captured screenshots.

## Prerequisites

The project requires Python 3.12+ and all dependencies are managed through `pyproject.toml` and can be installed using the Makefile commands.

## Setup

### Running with Docker Compose

The application runs as two separate containers: a crawler and a dashboard. Start all services using:

```bash
make compose
```

This starts:
- **Dashboard**: Web interface at `http://localhost:8000`
- **Crawler**: Background service for crawling websites
- **Neo4j Database**: Web interface at `http://localhost:7474`, database at `bolt://localhost:7687`
- **Selenium**: Chrome browser for screenshot capture

To stop all services:

```bash
make stop
```

### Local Development Setup

For local development without Docker, you need to run two separate processes:

#### Prerequisites

1. Start a Neo4j database (can use Docker or devcontainer):
```bash
docker run -p 7474:7474 -p 7687:7687 -e NEO4J_AUTH=neo4j/password neo4j:latest
```

2. Configure environment:
```bash
cp .env.example .env
```

Edit `.env` with your Neo4j credentials:
```
NEO4j_URI="neo4j://localhost:7687"
NEO4j_USERNAME="neo4j"
NEO4j_PASSWORD="password"
```

3. Install dependencies:
```bash
make install
```

#### Running Locally

In separate terminals, run:

**Terminal 1 - Dashboard:**
```bash
uvicorn dashboard.api:app --host 0.0.0.0 --port 8000
```

**Terminal 2 - Crawler:**
```bash
python src/webmap/main.py
```

The dashboard will be accessible at `http://localhost:8000`.
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
Note, if you want to be able to see these tings on the webpage as well, you will have to write a "plugin" web. You can see how that is done in screenshot and boungingbox, for examples. 

### Web Dashboard

The dashboard container provides a web interface accessible at `http://localhost:8000` when running with Docker Compose. The dashboard provides real-time crawling statistics, crawler control, and screenshot viewing capabilities.

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
src/
├── webmap/                 # Crawler application
│   ├── main.py            
│   ├── screenshot/         # Screenshot capture
│   ├── boundingbox/        # Bounding box detection
│   └── database/           # Neo4j database integration
├── dashboard/              # Dashboard application
│   ├── api.py              # FastAPI web interface
│   ├── screenshot/         # Screenshot web plugin
│   └── boundingbox/        # Bounding box web plugin
containers/
├── crawler/                # Crawler Docker container
└── dashboard/              # Dashboard Docker container
tools/                      # Utility scripts
```

## Contributions

Allowed to add anything you want, please follow resonable standards and the ones found in [docs](./docs/).

## License

**Author**: Uplink036

This project is licensed under the [MIT License](./LICENSE).