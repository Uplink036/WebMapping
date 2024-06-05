import responses
import requests
import pytest
from unittest import mock
from webmap import Crawler, get_HTML_response
from hypothesis import given, strategies as st

attrs = {"content.return_value":"""  
                                <div>
                                    <p>lorem</p>
                                </div>"""}
HTML_EXAMPLE_CONTENT = mock.MagicMock(**attrs)

@responses.activate
@given(st.from_regex(r"[a-zA-Z][a-zA-Z/.?+]*", fullmatch=True))
def test_fuzz_Crawler(domain) -> None:
    url = "https://" + domain
    crawlerObject = Crawler(url=url)
    responses.add(
        responses.GET,
        url,
        body="hello world",
        status=404,
    )

    with mock.patch('webmap.crawler.plot_nodes') as mock_plot:
        crawlerObject.run()
        mock_plot.assert_called_once()

if __name__ == "__main__":
    pytest.main(["test/test_crawler.py"])