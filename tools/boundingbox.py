#!/usr/bin/env python3
"""Tool that will take and retrive from database a "boundingbox"""
import sys
import io
from PIL import Image

import sys
from webmap.boundingbox import BoundingBoxCapture, BoundingBoxDB

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python boundingbox <url> [filename]")
        sys.exit(1)
    
    url = sys.argv[1]
    filename = sys.argv[2] if len(sys.argv) > 2 else "screenshot.png"

    bBoxCapture = BoundingBoxCapture()

    image: bytes = bBoxCapture.take_bbox_screenshot(url)
    if image:
        with open(filename, 'wb') as f:
            f.write(image)
        print(f"Screenshot saved to {filename}")
    else:
        print("Failed to capture screenshot")
    bBoxCapture.close()