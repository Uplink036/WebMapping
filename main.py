import sys
import time
import uvicorn
from threading import Thread
from webmap import Crawler
from webmap.database import Neo4JControl

URL = "https://scrapeme.live/shop/"

crawler = Crawler(URL)
control = Neo4JControl()

if __name__ == "__main__":
    control.set_status(True)
    control.set_time(0.2)
    crawler_thread = Thread(target=lambda: Crawler(URL).run())
    crawler_thread.start()
    
    try:
        uvicorn.run("webmap.api:app", host="0.0.0.0", port=8000)
    except KeyboardInterrupt:
        print("Shutting down...")
        control.set_status(False)
        crawler_thread.join(timeout=5) 
        sys.exit(0)