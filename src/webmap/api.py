from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from webmap.database.database import Neo4JGraph, Neo4JStack


app = FastAPI(title="WebMapping API")


@app.get("/", response_class=HTMLResponse)
async def dashboard():
    stack = Neo4JStack()
    graph = Neo4JGraph()
    
    stack_count = stack.count()
    websites_count = graph.count()
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>WebMapping Dashboard</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 40px; }}
            .stat {{ background: #f5f5f5; padding: 20px; margin: 10px 0; border-radius: 5px; }}
            .number {{ font-size: 2em; font-weight: bold; color: #333; }}
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
    </body>
    </html>
    """
    return html


@app.get("/api/stats")
async def get_stats():
    stack = Neo4JStack()
    graph = Neo4JGraph()
    
    return {
        "stack_count": stack.count(),
        "websites_count": graph.count()
    }
