import time
from PIL import Image
from io import BytesIO

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from webmap.screenshot.database import ScreenshotDB

SERVER = "http://selenium:4444/wd/hub"


class ScreenshotCapture:
    def __init__(self) -> None:
        self.db = ScreenshotDB()
        self._setup_driver()

    def _setup_driver(self) -> None:
        """Setup remote Chrome driver."""
        options = Options()
        options.add_argument("--no-sandbox")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument('--disable-notifications')
        
        prefs = {
            "profile.default_content_setting_values.cookies": 2,
            "profile.block_third_party_cookies": True
        }
        options.add_experimental_option("prefs", prefs)

        self.driver = webdriver.Remote(command_executor=SERVER, options=options)

    def take_screenshot(self, url: str) -> bytes | None:
        """Take screenshot of URL and return as bytes."""
        try:
            self.driver.get(url)
            return self._fullpage_screenshot()
        except Exception as e:
            print(f"Screenshot Error: taking screenshot of {url}: {e}")
            return None
        
    def _fullpage_screenshot(self, scroll_delay: float = 0.3) -> bytes:
        """
        Takes a fullscreen pageshot
        """
        device_pixel_ratio = self.driver.execute_script('return window.devicePixelRatio')

        total_height = self.driver.execute_script('return document.body.parentNode.scrollHeight')
        viewport_height = self.driver.execute_script('return window.innerHeight')
        total_width = self.driver.execute_script('return document.body.offsetWidth')
        viewport_width = self.driver.execute_script("return document.body.clientWidth")

        assert(viewport_width == total_width)

        offset = 0
        slices = {}
        while offset < total_height:
            if offset + viewport_height > total_height:
                offset = total_height - viewport_height

            self.driver.execute_script('window.scrollTo({0}, {1})'.format(0, offset))
            time.sleep(scroll_delay)

            img = Image.open(BytesIO(self.driver.get_screenshot_as_png()))
            slices[offset] = img

            offset = offset + viewport_height

        stitched_image = Image.new('RGB', (total_width * device_pixel_ratio, total_height * device_pixel_ratio))
        for offset, image in slices.items():
            stitched_image.paste(image, (0, offset * device_pixel_ratio))
        img_byte_arr = BytesIO()
        stitched_image.save(img_byte_arr, format='PNG')
        img_byte_arr = img_byte_arr.getvalue()
        return img_byte_arr

    def capture_and_save(self, url: str) -> bool:
        """Take screenshot and save to database."""
        screenshot_data = self.take_screenshot(url)
        if screenshot_data:
            return self.db.save_screenshot(url, screenshot_data)
        return False

    def close(self) -> None:
        """Close the webdriver."""
        self.driver.quit()

    def __del__(self) -> None:
        self.close()
