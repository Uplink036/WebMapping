#!/usr/bin/env python3
"""Tool that will take a screenshot of a URL"""

import sys

from webmap.screenshot import ScreenshotCapture

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python screenshot.py <url> [filename]")
        sys.exit(1)

    url = sys.argv[1]
    filename = sys.argv[2] if len(sys.argv) > 2 else "screenshot.png"

    capture = ScreenshotCapture()

    image = capture.take_screenshot(url)
    if image:
        with open(filename, "wb") as f:
            f.write(image)
        print(f"Screenshot saved to {filename}")
    else:
        print("Failed to capture screenshot")
