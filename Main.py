from Map import plot_nodes
from Node import Node
from Scrapper import getHTMLResponse, getSoup, printParsedHTML, getAllLinks
from Url_Handling import getNameFromURL

def main():
    URL = "https://deviceatlas.com/blog/list-of-user-agent-strings#desktop"
    websites = {}
    visited_websites = {}
    urls = [URL]
    while len(urls) > 0 and len(websites) < 100:
        url = urls.pop(0)
        website_name = getNameFromURL(url)
        if website_name not in websites:
            websites[website_name] = Node(website_name)
        
        if website_name in visited_websites:
            continue

        html_response = getHTMLResponse(url)
        soup = getSoup(html_response)
        links = getAllLinks(soup)

        for link in links:
            link_website_name = getNameFromURL(link)
            if link_website_name is not None:
                urls.append(link)
                if link_website_name not in websites:
                    websites[link_website_name] = Node(link_website_name)
                websites[website_name].add_edge(websites[link_website_name])
        
        visited_websites[website_name] = True
            
    plot_nodes(websites[getNameFromURL(URL)])

if __name__ == "__main__":
    main()