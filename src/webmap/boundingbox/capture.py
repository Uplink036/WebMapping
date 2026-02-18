import io

from PIL import Image, ImageDraw
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from webmap.screenshot import ScreenshotCapture
from webmap.boundingbox.bbox import BBox
from webmap.boundingbox.database import BoundingBoxDB


class BoundingBoxCapture(ScreenshotCapture):
    def __init__(self) -> None:
        super().__init__()
        self.db = BoundingBoxDB()
        self._loaded_page = ""

    def load_page(self, url: str) -> None:
        try:
            self.driver.get(url)
            self._loaded_page = url
        except Exception as e:
            print(f"BoundingBox Error: taking screenshot of {url}: {e}")
        return None

    def take_clean_screenshot(self, url: str) -> bytes | None:
        """Take screenshot of URL and return as bytes."""
        if url is not self._loaded_page:
            self.load_page(url)
        return self.take_screenshot(url)

    def take_bbox_screenshot(self, url: str) -> bytes | None:
        """Take screenshot of URL and return as bytes."""
        if url is not self._loaded_page:
            self.load_page(url)
        try:
            screenshot_png = self.driver.get_screenshot_as_png()
            image = Image.open(io.BytesIO(screenshot_png))
            buttons = self.get_all_by_xpath(url, "//button")
            textarea = self.get_all_by_xpath(url, "//textarea")
            elements = buttons + textarea
            draw = ImageDraw.Draw(image)
            for element in elements:
                bbox: BBox = self.get_bbox(element)
                if (
                    abs(bbox.x_max - bbox.x_min) <= 5
                    and abs(bbox.y_max - bbox.y_min) <= 5
                ):
                    continue
                draw.rectangle(
                    [bbox.x_min, bbox.y_min, bbox.x_max, bbox.y_max],
                    outline="red",
                    width=2,
                )
            new_image = io.BytesIO()
            image.save(new_image, "PNG")
            new_image.seek(0)
            return new_image.getvalue()
        except Exception as e:
            print(f"BoundingBox Error: taking screenshot of {url}: {e}")
            return None

    def get_html(self, url: str) -> str:
        if url is not self._loaded_page:
            self.load_page(url)
        try:
            html = self.driver.page_source
            return html
        except Exception as e:
            print(f"BoundingBox Error: getting html source {url}: {e}")
            return ""

    def get_all_by_xpath(self, url: str, x_string: str) -> list[WebElement]:
        if url is not self._loaded_page:
            self.load_page(url)
        try:
            buttons = self.driver.find_elements(By.XPATH, x_string)
            return buttons
        except Exception as e:
            print(f"BoundingBox Error: getting all by x path {url}: {e}")
            return []

    def get_bbox(self, element: WebElement) -> BBox:
        location = element.location
        size = element.size
        x, y = location["x"], location["y"]
        width, height = size["width"], size["height"]
        bbox = BBox(x, y, x + width, y + height, element.text, element.tag_name)
        return bbox

    def capture_and_save(self, url: str) -> bool:
        """Take screenshots and save bounding box data to database."""
        if url != self._loaded_page:
            self.load_page(url)

        clean_screenshot = self.take_clean_screenshot(url)

        buttons = self.get_all_by_xpath(url, "//button")
        textarea = self.get_all_by_xpath(url, "//textarea")

        elements = buttons + textarea
        bounding_boxes = (
            [self.get_bbox(element) for element in elements] if elements else []
        )

        bbox_screenshot = self.take_bbox_screenshot(url)

        success = True
        if clean_screenshot is None:
            success &= self.db.save_screenshot(url, b"error", "clean-error")
        else:
            success &= self.db.save_screenshot(url, clean_screenshot, "clean")
        if bbox_screenshot is None:
            success &= self.db.save_screenshot(url, b"error", "clean-error")
        else:
            success &= self.db.save_screenshot(url, bbox_screenshot, "bbox")
        success &= self.db.save_bounding_boxes(url, bounding_boxes)

        return success