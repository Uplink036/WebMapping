from .map import plot_nodes
from .node import Node
from .scraper import get_HTML_response, get_soup, print_parsed_HTML, get_all_links
from .url_handling import get_name_from_URL


class Crawler:
    def __init__(self, url) -> None:
        self.starting_url = url

    def run(self):
        if self.starting_url is None:
            raise ValueError
        
        websites = {}
        visited_websites = {}
        urls = [self.starting_url]
        while len(urls) > 0 and len(websites) < 100:
            url = urls.pop(0)
            website_name = get_name_from_URL(url)
            if website_name not in websites:
                websites[website_name] = Node(website_name)
            
            if website_name in visited_websites:
                continue

            html_response = get_HTML_response(url)
            soup = get_soup(html_response)
            links = get_all_links(soup)

            for link in links:
                link_website_name = get_name_from_URL(link)
                if link_website_name is not None:
                    urls.append(link)
                    if link_website_name not in websites:
                        websites[link_website_name] = Node(link_website_name)
                    websites[website_name].add_edge(websites[link_website_name])
            
            visited_websites[website_name] = True
                
        plot_nodes(websites[get_name_from_URL(self.starting_url)])
