from webmap.database.database import Neo4JGraph, Neo4JStack
from webmap.map import plot_nodes
from webmap.node import Node
from webmap.scraper import get_all_links, get_HTML_response, get_soup
from webmap.url_handling import get_name_from_URL


class Crawler:
    def __init__(self, url=None) -> None:
        self.starting_url: str = url
        self._graph: Neo4JGraph = Neo4JGraph()
        self._stack: Neo4JStack = Neo4JStack()

    def run(self) -> None:
        if self._stack.count() == 0:
            if self.starting_url is None:
                raise ValueError
            self._stack.push(self.starting_url)

        while self._stack.count() > 0:
            url = self._stack.pop()
            if url is None:
                raise ValueError("Crawler error: Stack returned unexpected value")
            website_name = get_name_from_URL(url)
            if not self._graph.in_database(website_name):
                self._graph.add_node(website_name)

            if self._graph.in_database(website_name):
                links = self._fetch_links(url)
                for element in self._parse_links(website_name, links):
                    self._stack.push(element)

    def _parse_links(
        self, website_origin: str, list_with_links: list[str]
    ) -> list[str]:
        found_urls = []
        for link in list_with_links:
            link_website_name = get_name_from_URL(link)
            if link_website_name is None:
                continue

            found_urls.append(link)
            if not self._graph.in_database(link_website_name):
                self._graph.add_node(link_website_name)

            self._graph.add_edge(website_origin, link_website_name)
        return found_urls

    def _fetch_links(self, url: str | None = None) -> list[str]:
        """
        Provided with a url, it will get get all the links on that html page and send them back as a list.
        """
        html_response = get_HTML_response(url)
        soup = get_soup(html_response)
        return get_all_links(soup)
