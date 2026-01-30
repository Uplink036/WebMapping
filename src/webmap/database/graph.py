from webmap.database.base import Database


class GraphDB(Database):
    def __init__(self) -> None:
        super().__init__()

    def add_node(self, url: str) -> bool:
        raise NotImplementedError

    def add_edge(self, from_website: str, to_website: str) -> bool:
        raise NotImplementedError

    def count(self) -> int:
        raise NotImplementedError

    def in_database(self, url: str) -> bool:
        raise NotImplementedError


class Neo4JGraph(GraphDB):
    def __init__(self) -> None:
        super().__init__()

    def add_node(self, url: str) -> bool:
        with self._driver.session() as session:
            result = session.run("MERGE (w:Website {url: $url}) RETURN w", url=url)
            return result.single() is not None

    def add_edge(self, from_website: str, to_website: str) -> bool:
        with self._driver.session() as session:
            result = session.run(
                """
                MATCH (a:Website {url: $from_site})
                MATCH (b:Website {url: $to_site})
                MERGE (a)-[:LINKS_TO]->(b)
                RETURN a, b
            """,
                from_site=from_website,
                to_site=to_website,
            )
            return result.single() is not None

    def count(self) -> int:
        with self._driver.session() as session:
            result = session.run("MATCH (w:Website) RETURN count(w) as count")
            record = result.single()
            if not record:
                return 0
            count: int = record["count"]
            return count

    def in_database(self, url: str) -> bool:
        with self._driver.session() as session:
            result = session.run("MATCH (w:Website {url: $url}) RETURN w", url=url)
            return result.single() is not None
