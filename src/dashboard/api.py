import random
import time
from typing import Callable, Dict, List, Union

from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse, Response
from pydantic import BaseModel

from webmap.database import Neo4JControl, Neo4JGraph, Neo4JStack
from webmap.screenshot.database import ScreenshotDB

app = FastAPI(title="WebMapping API")

plugin_sections: List[Callable[[], str]] = []


def register_plugin_section(section_func: Callable[[], str]) -> None:
    """Register a plugin section for the dashboard."""
    plugin_sections.append(section_func)


class URLRequest(BaseModel):
    url: str


@app.get("/", response_class=HTMLResponse)
async def dashboard() -> str:
    stack = Neo4JStack()
    graph = Neo4JGraph()
    control = Neo4JControl()

    stack_count = stack.count()
    websites_count = graph.count()
    status = control.get_status()
    sleep_time = control.get_time()

    plugin_html = ""
    for section_func in plugin_sections:
        plugin_html += section_func()

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
            .plugin-section {{ background: #e8f4f8; padding: 20px; margin: 20px 0; border-radius: 5px; border-left: 4px solid #007acc; }}
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
            <button onclick="fetch('/api/set_status?status=true').then(() => location.reload())">Start Crawler</button>
            <button onclick="fetch('/api/set_status?status=false').then(() => location.reload())">Stop Crawler</button>
            <button onclick="setSleepTime()">Set Sleep Time</button>
        </div>
        {plugin_html}
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


@app.get("/api/random_screenshot")
async def get_random_screenshot(screenshot_type: str = Query("clean")) -> Response:
    """Get a random screenshot from the database."""
    db = ScreenshotDB()

    with db._driver.session() as session:
        if screenshot_type == "bbox":
            result = session.run(
                "MATCH (s:Screenshot {type: 'bbox'}) RETURN s.url as url"
            )
        else:
            result = session.run(
                "MATCH (s:Screenshot) WHERE s.type IS NULL OR s.type = 'clean' RETURN s.url as url"
            )
        urls = [record["url"] for record in result]

    if not urls:
        return Response(
            content=f"No {screenshot_type} screenshots available", status_code=404
        )

    random_url = random.choice(urls)
    screenshot_data = db.get_screenshot(random_url, screenshot_type)

    if screenshot_data:
        return Response(content=screenshot_data, media_type="image/png")
    else:
        return Response(content="Screenshot not found", status_code=404)


# Register plugin sections
try:
    from interface.screenshot.web import screenshot_section

    register_plugin_section(screenshot_section)
except ImportError:
    pass

try:
    from interface.boundingbox.web import boundingbox_section

    register_plugin_section(boundingbox_section)
except ImportError:
    pass
