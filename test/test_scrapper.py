import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from unittest import mock

from src.Scrapper import get_HTML_response, get_soup, get_all_links, print_parsed_HTML

class TestScrapper():
    def test_get_HTML_response(self):
        url = "https://www.google.com"
        with mock.patch('src.Scrapper.requests.get') as mock_get:
            get_HTML_response(url)
            mock_get.assert_called_with(url=url, headers={'User-Agent': "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:15.0) Gecko/20100101 Firefox/15.0.1"})
if __name__ == "__main__":
    pytest.main()