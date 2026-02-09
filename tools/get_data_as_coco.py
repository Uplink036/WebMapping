#!/usr/bin/env python3
"""Tool to retrieve screenshots from database and save to file."""

import io
import pathlib
import shutil
import sys

import yaml
from neo4j import GraphDatabase
from PIL import Image
from tqdm import tqdm

from webmap.boundingbox import BoundingBoxDB
from webmap.database.constants import AUTH_PASSWORD, AUTH_USERNAME, DATABASE_URI

ROOT_DIR = pathlib.Path("./CV_WebMapping")
TRAIN_DIR = ROOT_DIR / "train"
TEST_DIR = ROOT_DIR / "test"
VAL_DIR = ROOT_DIR / "val"


def get_safe_filename(url):
    safe_url = url.replace("://", "_").replace("/", "_").replace("?", "_")
    filename = f"screenshot_{safe_url}.png"
    return filename


def save_screenshot_from_db(url: str, dir: pathlib.Path) -> str:
    """Retrieve screenshot from database and save to file."""
    filename = get_safe_filename(url)

    db = BoundingBoxDB()
    screenshot_data = db.get_screenshot(url, "clean")

    if screenshot_data is None:
        print(f"No screenshot found for URL: {url}")
        return None

    try:
        with open(dir / filename, "wb") as f:
            f.write(screenshot_data)
    except Exception as e:
        print(f"Error saving file: {e}")


def save_bbox_from_db(url: str, dir: pathlib.Path) -> None:
    db = BoundingBoxDB()
    bboxs = db.get_bounding_boxes(url)

    screenshot_data = db.get_screenshot(url, "clean")
    if screenshot_data is None:
        return None

    img = Image.open(io.BytesIO(screenshot_data))
    img_width, img_height = img.size

    label_file = get_safe_filename(url)

    with open(label_file, "w") as f:
        for bbox in bboxs:
            x_center, y_center, width, height, class_id = convert_into_coco_bbox(
                img_width, img_height, bbox
            )
            f.write(f"{class_id} {x_center} {y_center} {width} {height}\n")


def convert_into_coco_bbox(img_width, img_height, bbox):
    x_min, y_min, x_max, y_max = bbox.x_min, bbox.y_min, bbox.x_max, bbox.y_max

    x_center = ((x_min + x_max) / 2) / img_width
    y_center = ((y_min + y_max) / 2) / img_height
    width = (x_max - x_min) / img_width
    height = (y_max - y_min) / img_height

    class_id = list(data["name"].values()).index(bbox.name)
    return x_center, y_center, width, height, class_id


if __name__ == "__main__":
    db = BoundingBoxDB()
    driver = GraphDatabase.driver(DATABASE_URI, auth=(AUTH_USERNAME, AUTH_PASSWORD))

    data: dict = {}

    data["path"] = "CV_WebMapping"
    TRAIN_DIR.mkdir(parents=True, exist_ok=True)
    data["train"] = "train"
    TEST_DIR.mkdir(parents=True, exist_ok=True)
    data["test"] = "test"
    VAL_DIR.mkdir(parents=True, exist_ok=True)
    data["val"] = "val"

    try:
        with driver.session() as session:
            results = session.run(
                "MATCH (n:BoundingBox) RETURN DISTINCT n.element_type"
            )
            data["names"] = {
                index: type for index, type in enumerate(results.values()[0])
            }

        with driver.session() as session:
            results = session.run("MATCH (n:Page) RETURN DISTINCT n.url ")
            urls = results.value()

        for index, url in tqdm(enumerate(urls)):
            if index < 10:
                current_dir = VAL_DIR
            else:
                current_dir = TRAIN_DIR if index <= len(urls) * 0.8 else TEST_DIR
            save_screenshot_from_db(url, current_dir)
            save_bbox_from_db(url, current_dir)

        with open("coco8.yaml", "w") as outfile:
            yaml.dump(data, outfile, default_flow_style=False)
    finally:
        driver.close()

    if "--zip" in sys.argv:
        shutil.make_archive("CV_WebMapping", "zip", ROOT_DIR)
        shutil.rmtree(ROOT_DIR)
        print("Created CV_WebMapping.zip")
