import sys
import threading
import uvicorn
from time import sleep
from webmap import Crawler

URL = "https://scrapeme.live/shop/"

if __name__ == "__main__":
    # Start API in background thread
    api_thread = threading.Thread(target=lambda: uvicorn.run("webmap.api:app", host="0.0.0.0", port=8000))
    api_thread.start()
    
    # Start crawler in background thread
    crawler_thread = threading.Thread(target=lambda: Crawler(URL).run())
    crawler_thread.start()
    
    # Keep main thread alive
    try:
        while True:
            sleep(1)
    except KeyboardInterrupt:
        print("Shutting down...")
        sys.exit(0)