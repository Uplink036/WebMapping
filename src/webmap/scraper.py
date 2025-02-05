import requests 
from bs4 import BeautifulSoup 

def get_HTML_response(url):
    headers = {'User-Agent': "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:15.0) Gecko/20100101 Firefox/15.0.1"} 
    html_response = requests.get(url=url, headers=headers)
    return html_response

def get_soup(html_response):
    soup = BeautifulSoup(html_response.content, 'html5lib')
    return soup

def get_all_links(soup):
    links = [link.get('href') for link in soup.find_all('a')]
    return links

def print_raw_HTML(html_response):
    raw_html = html_response.content
    print(raw_html)

def print_parsed_HTML(raw_html):
    soup = BeautifulSoup(raw_html, 'html5lib') # If this line causes an error, run 'pip install html5lib' or install html5lib 
    print(soup.prettify())

