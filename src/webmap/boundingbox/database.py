import base64

from webmap.boundingbox.bbox import BBox
from webmap.database.base import Database


class BoundingBoxDB(Database):
    def __init__(self) -> None:
        super().__init__()

    def save_screenshot(
        self, url: str, screenshot_data: bytes, screenshot_type: str = ""
    ) -> bool:
        """Save screenshot data to database with proper relationships."""
        with self._driver.session() as session:
            screenshot_b64 = base64.b64encode(screenshot_data).decode("utf-8")

            website = url

            session.run(
                """MERGE (p:Page {url: $url}) 
                   SET p.timestamp = datetime()
                   WITH p
                   MATCH (w:Website {url: $website})
                   MERGE (w)-[:HAS_PAGE]->(p)""",
                url=url,
                website=website,
            )

            result = session.run(
                """MERGE (s:Screenshot {url: $url, type: $type}) 
                   SET s.data = $data, s.timestamp = datetime()
                   WITH s
                   MATCH (p:Page {url: $url})
                   MERGE (p)-[:HAS_SCREENSHOT]->(s)
                   RETURN s""",
                url=url,
                type=screenshot_type,
                data=screenshot_b64,
            )
            return result.single() is not None

    def save_bounding_boxes(self, url: str, bounding_boxes: list[BBox]) -> bool:
        """Save bounding box data as BoundingBox nodes."""
        with self._driver.session() as session:
            website = url
            session.run(
                """MERGE (p:Page {url: $url}) 
                   SET p.timestamp = datetime()
                   WITH p
                   MATCH (w:Website {url: $website})
                   MERGE (w)-[:HAS_PAGE]->(p)""",
                url=url,
                website=website,
            )

            for i, bbox in enumerate(bounding_boxes):
                session.run(
                    """MATCH (p:Page {url: $url})
                       CREATE (b:BoundingBox {
                           element_type:  $tag,
                           element_text: $text,
                           index: $index,
                           x_min: $x_min,
                           y_min: $y_min,
                           x_max: $x_max,
                           y_max: $y_max,
                           width: $width,
                           height: $height
                       })
                       CREATE (p)-[:HAS_BBOX]->(b)""",
                    tag=bbox.name,
                    text=bbox.text,
                    url=url,
                    index=i,
                    x_min=bbox.x_min,
                    y_min=bbox.y_min,
                    x_max=bbox.x_max,
                    y_max=bbox.y_max,
                    width=bbox.x_max - bbox.x_min,
                    height=bbox.y_max - bbox.y_min,
                )
            return True

    def get_screenshot(self, url: str, screenshot_type: str = "clean") -> bytes | None:
        """Retrieve screenshot data from database."""
        with self._driver.session() as session:
            if screenshot_type != "clean":
                result = session.run(
                    f'MATCH (s:Screenshot) WHERE s.url = "{url}" AND s.type = "{screenshot_type}" RETURN s.data as data'
                )
            else:
                result = session.run(
                    "MATCH (s:Screenshot {url: $url}) WHERE s.type IS NULL OR s.type = 'clean' RETURN s.data as data",
                    url=url,
                )

            record = result.single()
            if record and record["data"]:
                return base64.b64decode(record["data"])
            return None


    def get_bounding_boxes(self, url: str) -> list[BBox]:
        """Retrieve BoundingBox nodes for a page."""
        with self._driver.session() as session:
            result = session.run(
                """MATCH (p:Page {url: $url})-[:HAS_BBOX]->(b:BoundingBox)
                   RETURN b.x_min as x_min, b.y_min as y_min, 
                          b.x_max as x_max, b.y_max as y_max,
                          b.element_text as text, b.element_type as name
                   ORDER BY b.index""",
                url=url,
            )
            return [BBox(**record.data()) for record in result]
