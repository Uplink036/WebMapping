import requests 
from bs4 import BeautifulSoup 

URL = "https://scrapeme.live/shop/"
headers = {'User-Agent': "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:15.0) Gecko/20100101 Firefox/15.0.1"} 
# Here the user agent is for Edge browser on windows 10. You can find your browser user agent from the above given link. 
html_response = requests.get(url=URL, headers=headers)  
raw_html = html_response.content
soup = BeautifulSoup(raw_html, 'html5lib') # If this line causes an error, run 'pip install html5lib' or install html5lib 
print(soup.prettify()) 


links = []

# Find all the links in the page
for link in soup.find_all('a'):
    links.append(link.get('href'))

print(links)