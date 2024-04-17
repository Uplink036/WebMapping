
from links import links_to_websites
from Map import plot_web_map
from Node import Node
from Scrapper import getHTMLResponse, getSoup, printParsedHTML, getAllLinks


def main():
    URL = "https://scrapeme.live/shop/"
    websites = {}
    urls = [URL]
    while len(urls) > 0:
        url = urls.pop(0)
        
        website_name = getNameFromURL(url)
        if website_name not in websites:
            websites[website_name] = Node(website_name)
        else:
            continue


        html_response = getHTMLResponse(url)
        soup = getSoup(html_response)
        links = getAllLinks(soup)

        for link in links:
            website_name = getNameFromURL(link)
            if link is not None:
                urls.append(link)
                if website_name not in websites:
                    urls.append(link)
                    websites[website_name] = Node(website_name)
                websites[website_name].add_edge(websites[website_name])

        websites[website_name].visited = True
    

            


def getNameFromURL(url):
    if not checkIfURL(url):
        return None
    return url.split("//")[-1].split("/")[0]

def checkIfURL(url):
    return url.startswith("http://") or url.startswith("https://")

if __name__ == "__main__":
    main()