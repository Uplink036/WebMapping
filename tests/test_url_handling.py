import pytest 
from hypothesis import given, assume
from hypothesis import strategies as st
from webmap.url_handling import get_name_from_URL, isValidURL

class TestURLHandling():
    def test_is_valid_URL(self):
        assert isValidURL("https://www.google.com") == True
        assert isValidURL("http://www.google.com") == True
        assert isValidURL("www.google.com") == False
        assert isValidURL(None) == False

    @given(url=st.text())
    def test_fuzz_isValidURL(self, url):
        isValidURL(url=url)

    def test_get_name_from_URL(self):
        assert get_name_from_URL("https://www.google.com") == "www.google.com"
        assert get_name_from_URL("http://www.google.com") == "www.google.com"
        assert get_name_from_URL("www.google.com") == None
        assert get_name_from_URL(None) == None

    @given(url=st.text())
    def test_fuzz_get_name_from_URL(self, url):
        get_name_from_URL(url=url)

if __name__ == "__main__":
    pytest.main()