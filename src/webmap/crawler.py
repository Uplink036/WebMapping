from time import sleep
from typing import Callable, List

from webmap.database import Neo4JControl, Neo4JGraph, Neo4JStack, StatusDB
from webmap.scraper import get_all_links, get_HTML_response, get_soup
from webmap.url_handling import isValid


class Crawler:
    def __init__(self, url: str | None = None) -> None:
        self.starting_url: str | None = url
        self._graph: Neo4JGraph = Neo4JGraph()
        self._stack: Neo4JStack = Neo4JStack()
        self._control: Neo4JControl = Neo4JControl()
        self._status: StatusDB = StatusDB()
        self._plugins: List[Callable[[str], None]] = []

    def add(self, func: Callable[[str], None]) -> None:
        """Add a function to be applied to each URL."""
        self._plugins.append(func)

    def run(self) -> None:
        if self._stack.count() == 0:
            if self.starting_url is None:
                raise ValueError
            self._stack.push(self.starting_url)
            self._status.log_status(f"Crawler started with URL: {self.starting_url}")
            self._status.log_status(f"{self._plugins}")

        while self._control.get_status():
            if self._stack.count() > 0:
                url = self._stack.pop()
                if url is None:
                    self._status.log_status("Stack returned unexpected value")
                    continue

                if not isValid(url):
                    self._status.log_status(f"Invalid URL: {url}")
                    continue

                if not self._graph.in_database(url):
                    self._graph.add_node(url)

                for plugin in self._plugins:
                    try:
                        plugin(url)
                    except Exception as e:
                        self._status.log_status(f"Plugin error for {url}: {e}")

                links = self._fetch_links(url)
                for element in self._parse_links(url, links):
                    self._stack.push(element)
            sleep(self._control.get_time())

    def _parse_links(
        self, website_origin: str, list_with_links: list[str]
    ) -> list[str]:
        found_urls = []
        for link in list_with_links:
            if not isValid(link):
                continue

            found_urls.append(link)
            if not self._graph.in_database(link):
                self._graph.add_node(link)

            self._graph.add_edge(website_origin, link)
        return found_urls

    def _fetch_links(self, url: str | None = None) -> list[str]:
        """
        Provided with a url, it will get get all the links on that html page and send them back as a list.
        """
        if url is None:
            return []
        html_response = get_HTML_response(url)
        if html_response is None:
            return []
        soup = get_soup(html_response)
        return get_all_links(soup)
