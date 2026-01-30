import pytest
from hypothesis import assume, given
from hypothesis import strategies as st

from webmap.url_handling import get_name_from_URL, isValid


class TestURLHandling:
    def test_is_valid_URL(self):
        assert isValid("https://www.google.com") == True
        assert isValid("http://www.google.com") == True
        assert isValid("www.google.com") == False
        assert isValid(None) == False

    @given(url=st.text())
    def test_fuzz_isValidURL(self, url):
        isValid(url=url)

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
