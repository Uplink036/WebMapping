from typing import Any, cast

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


class ControlDB(Database):
    def __init__(self) -> None:
        super().__init__()

    def set_status(self, status: bool) -> None:
        raise NotImplementedError

    def get_status(self) -> bool:
        raise NotImplementedError

    def set_time(self, time: float) -> str | None:
        raise NotImplementedError

    def get_time(self) -> float:
        raise NotImplementedError


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

    def _item_exists(self, item: str) -> bool:
        with self._driver.session() as session:
            result = session.run(
                "MATCH (s) WHERE (s:StackItem OR s:CompletedStackItem) AND s.value = $item RETURN s",
                item=item,
            )
            return result.single() is not None

    def push(self, item: Any) -> None:
        item_str = str(item)
        if not self._item_exists(item_str):
            with self._driver.session() as session:
                session.run("CREATE (s:StackItem {value: $item})", item=item_str)

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


class Neo4JControl(ControlDB):
    def __init__(self) -> None:
        super().__init__()

    def set_status(self, status: bool) -> None:
        with self._driver.session() as session:
            session.run(
                "MERGE (c:Control {id: 'crawler'}) SET c.running = $status",
                status=status,
            )

    def get_status(self) -> bool:
        with self._driver.session() as session:
            result = session.run(
                "MATCH (c:Control {id: 'crawler'}) RETURN c.running as status"
            )
            record = result.single()
            if not record:
                return False
            status: bool = record["status"] is True
            return status

    def set_time(self, time: float) -> None:
        with self._driver.session() as session:
            session.run(
                "MERGE (c:Control {id: 'crawler'}) SET c.last_update = $time", time=time
            )

    def get_time(self) -> float:
        with self._driver.session() as session:
            result = session.run(
                "MATCH (c:Control {id: 'crawler'}) RETURN c.last_update as time"
            )
            record = result.single()
            return float(record["time"]) if record and record["time"] else 0.0


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
