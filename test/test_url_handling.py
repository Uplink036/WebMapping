import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pytest 
from src.Url_Handling import get_name_from_URL, isValidURL

class TestURLHandling():
    def test_is_valid_URL(self):
        assert isValidURL("https://www.google.com") == True
        assert isValidURL("http://www.google.com") == True
        assert isValidURL("www.google.com") == False
        assert isValidURL(None) == False

    def test_get_name_from_URL(self):
        assert get_name_from_URL("https://www.google.com") == "www.google.com"
        assert get_name_from_URL("http://www.google.com") == "www.google.com"
        assert get_name_from_URL("www.google.com") == None
        assert get_name_from_URL(None) == None

if __name__ == "__main__":
    pytest.main()