import pytest
from hypothesis import given, assume
from hypothesis import strategies as st
from unittest import mock

from webmap.Scraper import get_HTML_response, get_soup, get_all_links, print_parsed_HTML, print_raw_HTML

class TestScrapper():

    @given(st.from_regex(r"https://."))
    def test_get_HTML_response(self, url):
        with mock.patch('webmap.Scraper.requests.get') as mock_get:
            get_HTML_response(url)
            mock_get.assert_called_with(url=url, headers={'User-Agent': "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:15.0) Gecko/20100101 Firefox/15.0.1"})

    def test_get_soup(self):
        html_example_content = """  
                            <div>
                                <p>lorem</p>
                            </div>"""
        mock_html_response = mock.MagicMock()
        mock_html_response.content = html_example_content
        soup = get_soup(mock_html_response)
        assert soup is not None
        assert soup.find('p').text == 'lorem'

    def test_print_raw_html(self):
        html_example_content = """  
                            <div>
                                <p>lorem</p>
                            </div>"""
        mock_html_response = mock.MagicMock()
        mock_html_response.content = html_example_content

        with mock.patch('builtins.print') as mock_print:
            print_raw_HTML(mock_html_response)
            mock_print.assert_called_once()

    def test_get_all_links(self):
        html_example_content = """  
                            <div>
                                <a href="https://www.google.com">Google</a>
                                <a href="https://www.facebook.com">Facebook</a>
                            </div>"""
        mock_html_response = mock.MagicMock()
        mock_html_response.content = html_example_content
        soup = get_soup(mock_html_response)
        links = get_all_links(soup)
        assert links == ['https://www.google.com', 'https://www.facebook.com']

    def test_print_parsed_HTML(self):
        html_example_content = """  
                                <div>
                                    <p>lorem</p>
                                </div>"""
        with mock.patch('builtins.print') as mock_print:
            print_parsed_HTML(html_example_content)
            mock_print.assert_called_once()

if __name__ == "__main__":
    pytest.main()