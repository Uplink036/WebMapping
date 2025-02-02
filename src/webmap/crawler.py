from .database import init_db, init_edge_collection, init_node_collection
from .node import Node
from .scraper import get_HTML_response, get_soup, print_parsed_HTML, get_all_links
from .url_handling import get_name_from_URL
import pymongo
import uuid
class Crawler:
    def __init__(self, url = None, web_size = 100) -> None:
        self.starting_url = url
        self._max_websize = web_size
        self._websites = {}
        self._db = init_db()
        self._website_col = init_node_collection(self._db)
        self._links_col = init_edge_collection(self._db)


    def run(self):
        if self.starting_url is None:
            raise ValueError

        visited_websites = {}
        urls = [self.starting_url]
        while len(urls) > 0 and self._count_websites() < self._max_websize:
            url = urls.pop(0)
            website_name = get_name_from_URL(url)
            if not self._encounted_website(website_name):
                self._add_website(website_name)
                
            if website_name not in visited_websites:
                links = self._fetch_links(url)
                urls += self._parse_links(website_name, links)
                visited_websites[website_name] = True
                
        #plot_nodes(self._websites[get_name_from_URL(self.starting_url)])


    def _parse_links(self, website_origin, list_with_links):
        found_urls = []
        for link in list_with_links:
            link_website_name = get_name_from_URL(link)
            if link_website_name is None:
                continue

            found_urls.append(link)
            if not self._encounted_website(link_website_name): 
                self._add_website(link_website_name)

            self._add_website_link(website_origin, link_website_name)
        return found_urls


    def _fetch_links(self, url=None):
        """
        Provided with a url, it will get get all the links on that html page and send them back as a list.
        """
        html_response = get_HTML_response(url)
        soup = get_soup(html_response)
        return get_all_links(soup)
    

    def _encounted_website(self, website_name):
        occurences = self._website_col.count_documents({"label": website_name})
        return True if int(occurences) == 1 else False


    def _add_website(self, website_name):
        print(website_name)
        node = {
            'label': website_name
        }
        self._website_col.insert_one(node)


    def _add_website_link(self, origin, end):
        edge = {
            'source': origin,
            'target': end
        }
        self._links_col.insert_one(edge)


    def _count_websites(self):
        return self._website_col.count_documents({})
