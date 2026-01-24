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
