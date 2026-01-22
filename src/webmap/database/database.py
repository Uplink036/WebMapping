from typing import Any
from typing import cast
import neo4j
from neo4j import GraphDatabase

from webmap.database.connection import verify_connectivity
from webmap.database.constants import AUTH_PASSWORD, AUTH_USERNAME, DATABASE_URI


class Database:
    def __init__(self) -> None:
        if verify_connectivity() is False:
            raise ConnectionError(
                "Database error: Could not create connection to database"
            )
        self._driver = GraphDatabase.driver(
            DATABASE_URI, auth=(AUTH_USERNAME, AUTH_PASSWORD)
        )


class StackDB(Database):
    def __init__(self) -> None:
        super().__init__()

    def push(self, item: Any) -> None:
        raise NotImplementedError

    def pop(self) -> str | None:
        raise NotImplementedError

    def count(self) -> int:
        raise NotImplementedError


class GraphDB(Database):
    def __init__(self) -> None:
        super().__init__()

    def add_node(self, website: str) -> bool:
        raise NotImplementedError

    def add_edge(self, from_website: str, to_website: str) -> bool:
        raise NotImplementedError

    def count(self) -> int:
        raise NotImplementedError

    def in_database(self, website: str) -> bool:
        raise NotImplementedError


class Neo4JStack(StackDB):
    def __init__(self) -> None:
        super().__init__()

    def push(self, item: Any) -> None:
        with self._driver.session() as session:
            session.run("CREATE (s:StackItem {value: $item})", item=str(item))

    def pop(self) -> str | None:
        with self._driver.session() as session:
            result = session.run(
                "MATCH (s:StackItem) WITH s ORDER BY elementId(s) DESC LIMIT 1 RETURN s.value, elementId(s) as node_id"
            )
            record = result.single()
            if not record:
                return None

            value: str = record["s.value"]
            node_id = record["node_id"]

            session.run(
                "MATCH (s:StackItem) WHERE elementId(s) = $node_id SET s:CompletedStackItem REMOVE s:StackItem",
                node_id=node_id,
            )
            return value

    def count(self) -> int:
        with self._driver.session() as session:
            result = session.run("MATCH (s:StackItem) RETURN count(s) as count")
            record = result.single()
            if not record:
                return 0
            count: int = record["count"]
            return count


class Neo4JGraph(GraphDB):
    def __init__(self) -> None:
        super().__init__()

    def add_node(self, website: str) -> bool:
        with self._driver.session() as session:
            result = session.run(
                "MERGE (w:Website {name: $name}) RETURN w", name=website
            )
            return result.single() is not None

    def add_edge(self, from_website: str, to_website: str) -> bool:
        with self._driver.session() as session:
            result = session.run(
                """
                MATCH (a:Website {name: $from_site})
                MATCH (b:Website {name: $to_site})
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

    def in_database(self, website: str) -> bool:
        with self._driver.session() as session:
            result = session.run(
                "MATCH (w:Website {name: $name}) RETURN w", name=website
            )
            return result.single() is not None
