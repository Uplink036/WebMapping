import time
from time import sleep
from typing import Callable, List

from webmap.database import Neo4JControl, Neo4JGraph, Neo4JStack, StatusDB
from webmap.scraper import get_all_links, get_HTML_response, get_soup
from webmap.url_handling import is_valid


class Crawler:
    def __init__(self, url: str | None = None) -> None:
        self.starting_url: str | None = url
        self._graph: Neo4JGraph = Neo4JGraph()
        self._stack: Neo4JStack = Neo4JStack()
        self._control: Neo4JControl = Neo4JControl()
        self._status: StatusDB = StatusDB()
        self._plugins: List[Callable[[str], None]] = []
        self._stop_requested: bool = False

    def add(self, func: Callable[[str], None]) -> None:
        """Add a function to be applied to each URL."""
        self._plugins.append(func)

    def stop(self) -> None:
        """Stop the crawler."""
        self._stop_requested = True
        self._status.log_status("Crawler stop command received")

    def _should_run(self) -> bool:
        """Check if crawler should continue running."""
        return self._control.get_status() and not self._stop_requested

    def run(self) -> None:
        if self._stack.count() == 0:
            if self.starting_url is None:
                raise ValueError
            self._stack.push(self.starting_url)
            self._status.log_status(f"Crawler started with URL: {self.starting_url}")
            self._status.log_status(f"{self._plugins}")

        while self._should_run():
            start_time = time.time()
            if self._stack.count() > 0:
                url = self._stack.pop()
                if url is None:
                    self._status.log_status("Stack returned unexpected value")
                    continue

                if not is_valid(url):
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
            run_time = round(time.time() - start_time, 2)
            remaining_sleep_time = self._control.get_time() - run_time
            if remaining_sleep_time > 0:
                sleep(remaining_sleep_time)

    def _parse_links(
        self, website_origin: str, list_with_links: list[str]
    ) -> list[str]:
        found_urls = []
        for link in list_with_links:
            if not is_valid(link):
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
