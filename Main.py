from Map import plot_nodes
from Node import Node
from Scrapper import getHTMLResponse, getSoup, printParsedHTML, getAllLinks


def main():
    URL = "https://deviceatlas.com/blog/list-of-user-agent-strings#desktop"
    websites = {}
    urls = [URL]
    while len(urls) > 0 and len(websites) < 100:
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
            link_website_name = getNameFromURL(link)
            if link_website_name is not None:
                urls.append(link)
                if link_website_name not in websites:
                    urls.append(link)
                    websites[link_website_name] = Node(link_website_name)
                websites[website_name].add_edge(websites[link_website_name])

            
    plot_nodes(websites[getNameFromURL(URL)])


def getNameFromURL(url):
    if not checkIfURL(url):
        return None
    return url.split("//")[-1]

def checkIfURL(url):
    
    if url is None:
        return False
    return url.startswith("http://") or url.startswith("https://")

if __name__ == "__main__":
    main()