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
@given(st.text(
        alphabet=st.from_regex(regex=r"^https://.$", fullmatch=True),
        min_size=10,
    ))
def test_fuzz_Crawler(url) -> None:
    crawlerObject = Crawler(url=url)
    responses.add(
        responses.GET,
        url,
        body="hello world",
        status=404,
    )

    with mock.patch('webmap.Crawler.plot_nodes') as mock_plot:
        crawlerObject.run()

if __name__ == "__main__":
    pytest.main(["test/test_crawler.py"])