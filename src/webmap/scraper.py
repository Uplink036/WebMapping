import requests
from bs4 import BeautifulSoup
from requests import Response


def get_HTML_response(url) -> Response:
    headers = {'User-Agent': "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:15.0) Gecko/20100101 Firefox/15.0.1"} 
    html_response = requests.get(url=url, headers=headers)
    return html_response

def get_soup(html_response: Response) -> BeautifulSoup:
    soup = BeautifulSoup(html_response.content, 'html5lib')
    return soup

def get_all_links(soup: BeautifulSoup) -> list[str]:
    links = [link.get('href') for link in soup.find_all('a')]
    return links


def print_response(response: Response, raw: False = False) -> None:
    raw = response.content
    if not raw:
        soup = BeautifulSoup(raw, 'html5lib')
        print(soup.prettify())
    else:
        print(raw)
