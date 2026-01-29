import time
from typing import Dict, Union
import random

from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse, Response

from webmap.database import Neo4JControl, Neo4JGraph, Neo4JStack
from webmap.screenshot.database import ScreenshotDB

app = FastAPI(title="WebMapping API")


@app.get("/", response_class=HTMLResponse)
async def dashboard() -> str:
    stack = Neo4JStack()
    graph = Neo4JGraph()
    control = Neo4JControl()

    stack_count = stack.count()
    websites_count = graph.count()
    status = control.get_status()
    sleep_time = control.get_time()

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>WebMapping Dashboard</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 40px; }}
            .stat {{ background: #f5f5f5; padding: 20px; margin: 10px 0; border-radius: 5px; }}
            .number {{ font-size: 2em; font-weight: bold; color: #333; }}
            .controls {{ margin: 20px 0; }}
            button {{ padding: 10px 20px; margin: 5px; font-size: 16px; cursor: pointer; }}
            .status {{ color: {'green' if status else 'red'}; }}
        </style>
    </head>
    <body>
        <h1>WebMapping Dashboard</h1>
        <div class="stat">
            <div class="number">{stack_count}</div>
            <div>Websites in Stack</div>
        </div>
        <div class="stat">
            <div class="number">{websites_count}</div>
            <div>Websites Completed</div>
        </div>
        <div class="stat">
            <div class="number status">{'Running' if status else 'Stopped'}</div>
            <div>Crawler Status</div>
        </div>
        <div class="stat">
            <div class="number">{sleep_time}</div>
            <div>Sleep Time (seconds)</div>
        </div>
        <div class="controls">
            <button onclick="fetch('/api/set_status?status=false').then(() => location.reload())">Stop Crawler</button>
            <button onclick="setSleepTime()">Set Sleep Time</button>
        </div>
        <script>
            function setSleepTime() {{
                const time = prompt('Enter sleep time in seconds:');
                if (time) {{
                    fetch(`/api/set_crawler_sleep?time=${{time}}`).then(() => location.reload());
                }}
            }}
        </script>
    </body>
    </html>
    """
    return html


@app.get("/api/stats")
async def get_stats() -> Dict[str, int]:
    stack = Neo4JStack()
    graph = Neo4JGraph()
    return {"stack_count": stack.count(), "websites_count": graph.count()}


@app.get("/api/set_status")
async def set_crawler_status(status: bool = Query(...)) -> Dict[str, str]:
    control = Neo4JControl()
    control.set_status(status)
    return {"message": f"Crawler status set to {status}"}


@app.get("/api/set_crawler_sleep")
async def set_crawler_sleep(
    sleep_time: float = Query(..., alias="time")
) -> Dict[str, str]:
    control = Neo4JControl()
    control.set_time(sleep_time)
    return {"message": f"Crawler sleep time set to {sleep_time}"}


@app.get("/api/get_status")
async def get_crawler_status() -> Dict[str, bool]:
    control = Neo4JControl()
    return {"status": control.get_status()}


@app.get("/api/get_sleep_time")
async def get_crawler_sleep_time() -> Dict[str, Union[float, int]]:
    control = Neo4JControl()
    return {"sleep_time": control.get_time()}


@app.get("/screenshots", response_class=HTMLResponse)
async def screenshots_page() -> str:
    """Simple page to view a random screenshot."""
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Screenshots</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; text-align: center; }
            img { max-width: 80%; border: 1px solid #ccc; margin: 20px 0; }
            button { padding: 10px 20px; font-size: 16px; cursor: pointer; }
        </style>
    </head>
    <body>
        <h1>Website Screenshots</h1>
        <button onclick="loadRandomScreenshot()">Load Random Screenshot</button>
        <div id="screenshot-container">
            <p>Click the button to load a random screenshot</p>
        </div>
        <script>
            function loadRandomScreenshot() {
                fetch('/api/random_screenshot')
                    .then(response => {
                        if (response.ok) {
                            const container = document.getElementById('screenshot-container');
                            container.innerHTML = '<img src="/api/random_screenshot" alt="Random Screenshot">';
                        } else {
                            document.getElementById('screenshot-container').innerHTML = '<p>No screenshots available</p>';
                        }
                    });
            }
        </script>
    </body>
    </html>
    """
    return html


@app.get("/api/random_screenshot")
async def get_random_screenshot():
    """Get a random screenshot from the database."""
    db = ScreenshotDB()
    
    # Get all screenshots (simplified - in production you'd want pagination)
    with db._driver.session() as session:
        result = session.run("MATCH (s:Screenshot) RETURN s.url as url")
        urls = [record["url"] for record in result]
    
    if not urls:
        return Response(content="No screenshots available", status_code=404)
    
    # Pick random URL and get its screenshot
    random_url = random.choice(urls)
    screenshot_data = db.get_screenshot(random_url)
    
    if screenshot_data:
        return Response(content=screenshot_data, media_type="image/png")
    else:
        return Response(content="Screenshot not found", status_code=404)
