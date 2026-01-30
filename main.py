import sys
import time
import uvicorn
from threading import Thread
from webmap import Crawler
from webmap.database import Neo4JControl
from webmap.boundingbox import BoundingBoxCapture

URL = "https://scrapeme.live/shop/"

def capture_bounding_boxes(url: str) -> None:
    capture = BoundingBoxCapture()
    capture.capture_and_save(url)

crawler = Crawler(URL)
crawler.add(capture_bounding_boxes)
control = Neo4JControl()

if __name__ == "__main__":
    control.set_status(True)
    control.set_time(1)
    crawler_thread = Thread(target=lambda: crawler.run())
    crawler_thread.start()
    
    try:
        uvicorn.run("webmap.api:app", host="0.0.0.0", port=8000)
    except KeyboardInterrupt:
        print("Shutting down...")
        control.set_status(False)
        crawler_thread.join(timeout=5) 
        sys.exit(0)