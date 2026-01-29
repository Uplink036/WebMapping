import base64

from webmap.database.base import Database


class ScreenshotDB(Database):
    def __init__(self) -> None:
        super().__init__()

    def save_screenshot(self, url: str, screenshot_data: bytes) -> bool:
        """Save screenshot data to database."""
        with self._driver.session() as session:
            screenshot_b64 = base64.b64encode(screenshot_data).decode("utf-8")
            result = session.run(
                "MERGE (s:Screenshot {url: $url}) SET s.data = $data, s.timestamp = datetime() RETURN s",
                url=url,
                data=screenshot_b64,
            )
            return result.single() is not None

    def get_screenshot(self, url: str) -> bytes | None:
        """Retrieve screenshot data from database."""
        with self._driver.session() as session:
            result = session.run(
                "MATCH (s:Screenshot {url: $url}) RETURN s.data as data", url=url
            )
            record = result.single()
            if record and record["data"]:
                return base64.b64decode(record["data"])
            return None
