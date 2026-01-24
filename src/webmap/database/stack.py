from typing import Any

from webmap.database.base import Database


class StackDB(Database):
    def __init__(self) -> None:
        super().__init__()

    def push(self, item: Any) -> None:
        raise NotImplementedError

    def pop(self) -> str | None:
        raise NotImplementedError

    def count(self) -> int:
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
