#!/usr/bin/env python3
"""Tool to retrieve screenshots from database and save to file."""

import sys
from webmap.screenshot.database import ScreenshotDB


def save_screenshot_from_db(url: str, filename: str = None) -> str:
    """Retrieve screenshot from database and save to file."""
    if filename is None:
        safe_url = url.replace('://', '_').replace('/', '_').replace('?', '_')
        filename = f"screenshot_{safe_url}.png"
    
    db = ScreenshotDB()
    screenshot_data = db.get_screenshot(url)
    
    if screenshot_data is None:
        print(f"No screenshot found for URL: {url}")
        return None
    
    try:
        with open(filename, 'wb') as f:
            f.write(screenshot_data)
        print(f"Screenshot saved to: {filename}")
        return filename
    except Exception as e:
        print(f"Error saving file: {e}")
        return None


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python save_screenshot.py <url> [filename]")
        sys.exit(1)
    
    url = sys.argv[1]
    filename = sys.argv[2] if len(sys.argv) > 2 else None
    
    result = save_screenshot_from_db(url, filename)
    if result:
        print(f"Success! Screenshot saved as: {result}")
    else:
        print("Failed to save screenshot")
        sys.exit(1)
