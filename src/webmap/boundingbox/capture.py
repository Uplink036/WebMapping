import io
import time

from PIL import Image, ImageDraw
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from webmap.boundingbox.bbox import BBox
from webmap.boundingbox.database import BoundingBoxDB
from webmap.screenshot import ScreenshotCapture


class BoundingBoxCapture(ScreenshotCapture):
    def __init__(self) -> None:
        super().__init__()
        self.db: BoundingBoxDB = BoundingBoxDB()  # type: ignore[assignment]
        self._loaded_page = ""

    def _load_page(self, url: str) -> None:
        try:
            self.driver.get(url)
            self._loaded_page = url
        except Exception as e:
            print(f"BoundingBox Error: taking screenshot of {url}: {e}")
        return None

    def take_clean_screenshot(self, url: str) -> bytes | None:
        """Take screenshot of URL and return as bytes."""
        return self.take_screenshot(url)

    def take_bbox_screenshot(self, url: str) -> bytes | None:
        """Take screenshot of URL with bounding boxes drawn."""
        try:
            self.driver.execute_script("window.scrollTo(0, 0)")
            time.sleep(0.3)
            fixed_header_height = self._get_header_height()
            elements = self._collect_elements(url)
            bboxes = self._extract_bboxs(elements)

            screenshot_png = self._fullpage_screenshot()
            device_pixel_ratio = self.driver.execute_script(
                "return window.devicePixelRatio"
            )
            image = Image.open(io.BytesIO(screenshot_png))
            draw = ImageDraw.Draw(image)

            for bbox in bboxes:
                if (
                    abs(bbox.x_max - bbox.x_min) <= 5
                    and abs(bbox.y_max - bbox.y_min) <= 5
                ):
                    print("Below limit")
                    continue
                self._draw_bbox(fixed_header_height, device_pixel_ratio, draw, bbox)

            new_image = io.BytesIO()
            image.save(new_image, "PNG")
            new_image.seek(0)
            return new_image.getvalue()
        except Exception as e:
            print(f"BoundingBox Error: taking screenshot of {url}: {e}")
            return None

    def _draw_bbox(
        self,
        fixed_header_height: int,
        device_pixel_ratio: int,
        draw: ImageDraw.ImageDraw,
        bbox: BBox,
    ) -> None:
        y_min = (bbox.y_min + fixed_header_height) * device_pixel_ratio
        y_max = (bbox.y_max + fixed_header_height) * device_pixel_ratio
        draw.rectangle(
            [
                bbox.x_min * device_pixel_ratio,
                y_min,
                bbox.x_max * device_pixel_ratio,
                y_max,
            ],
            outline="red",
            width=2,
        )

    def _extract_bboxs(self, elements: list[WebElement]) -> list[BBox]:
        bboxes: list[BBox] = []

        for i, element in enumerate(elements):
            if not element.is_displayed():
                continue
            bbox = self.get_bbox(element)
            enabled = element.is_enabled()
            print(
                f"Element {i} ({bbox.name}): pos=[{bbox.x_min},{bbox.y_min}] size=[{bbox.x_max-bbox.x_min}x{bbox.y_max-bbox.y_min}] enabled={enabled} text='{bbox.text[:30]}'"
            )
            bboxes.append(bbox)
        return bboxes

    def _collect_elements(self, url: str) -> list[WebElement]:
        """Returns all the webelements of the current driver"""
        buttons = self.get_all_by_xpath(url, "//button")
        textarea = self.get_all_by_xpath(url, "//textarea")
        links = self.get_all_by_xpath(url, "//a")
        elements = buttons + textarea + links
        return elements

    def _get_header_height(self) -> int:
        """Returns the header height of the currennt driver"""
        fixed_header_height: int = self.driver.execute_script(
            """
                var maxHeight = 0;
                var elements = document.querySelectorAll('*');
                elements.forEach(function(el) {
                    var style = window.getComputedStyle(el);
                    if (style.position === 'fixed' || style.position === 'sticky') {
                        var rect = el.getBoundingClientRect();
                        if (rect.top === 0 && rect.height > maxHeight) {
                            maxHeight = rect.height;
                        }
                    }
                });
                return maxHeight;
            """
        )
        return fixed_header_height

    def get_html(self, url: str) -> str:
        if url is not self._loaded_page:
            self._load_page(url)
        try:
            html = self.driver.page_source
            return html
        except Exception as e:
            print(f"BoundingBox Error: getting html source {url}: {e}")
            return ""

    def get_all_by_xpath(self, url: str, x_string: str) -> list[WebElement]:
        if url is not self._loaded_page:
            self._load_page(url)
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

    def capture_and_save(self, url: str, fullpage: bool = True) -> bool:
        """Take screenshots and save bounding box data to database."""
        if url != self._loaded_page:
            self._load_page(url)

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
            success &= self.db.save_screenshot(url, b"error", "bbox-error")
        else:
            success &= self.db.save_screenshot(url, bbox_screenshot, "bbox")
        success &= self.db.save_bounding_boxes(url, bounding_boxes)

        return bool(success)
