import requests 
from bs4 import BeautifulSoup 

def getHTMLResponse(url):
    headers = {'User-Agent': "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:15.0) Gecko/20100101 Firefox/15.0.1"} 
    html_response = requests.get(url=URL, headers=headers)
    return html_response

def getAllLinks(html_response):
    soup = BeautifulSoup(html_response.content, 'html5lib')
    links = []
    for link in soup.find_all('a'):
        links.append(link.get('href'))
    return links

def printRawHTML(html_response):
    raw_html = html_response.content
    print(raw_html)

def printParsedHTML(raw_html):
    soup = BeautifulSoup(raw_html, 'html5lib') # If this line causes an error, run 'pip install html5lib' or install html5lib 
    print(soup.prettify())



if __name__ == "__main__":
    URL = "https://scrapeme.live/shop/"
    html_response = getHTMLResponse(URL)
    printParsedHTML(html_response.content)

    links = getAllLinks(html_response)
    print(links)