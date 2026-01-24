from webmap.database.base import Database


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
