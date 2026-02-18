from webmap import Crawler
from webmap.boundingbox import BoundingBoxCapture

URL = "https://scrapeme.live/shop/"

def capture_bounding_boxes(url: str) -> None:
    capture = BoundingBoxCapture()
    capture.capture_and_save(url)

if __name__ == "__main__":
    crawler = Crawler(URL)
    crawler.add(capture_bounding_boxes)
    crawler.run()
        