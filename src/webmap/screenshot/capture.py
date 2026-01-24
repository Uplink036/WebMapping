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
        
        # Connect to remote Selenium standalone container
        self.driver = webdriver.Remote(
            command_executor=SERVER,
            options=options
        )

    def take_screenshot(self, url: str) -> bytes | None:
        """Take screenshot of URL and return as bytes."""
        try:
            self.driver.get(url)
            screenshot_png = self.driver.get_screenshot_as_png()
            return screenshot_png
        except Exception as e:
            print(f"Screenshot Error: taking screenshot of {url}: {e}")
            return None

    def capture_and_save(self, url: str) -> bool:
        """Take screenshot and save to database."""
        screenshot_data = self.take_screenshot(url)
        if screenshot_data:
            return self.db.save_screenshot(url, screenshot_data)
        return False

    def close(self) -> None:
        """Close the webdriver."""
        self.driver.quit()
