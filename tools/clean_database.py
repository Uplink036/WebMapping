#!/usr/bin/env python3
"""Database cleaning script for WebMapping project."""

from neo4j import GraphDatabase, Session
from webmap.database.constants import AUTH_PASSWORD, AUTH_USERNAME, DATABASE_URI


def delete_realtionships(session: Session) -> None:
    session.run("MATCH ()-[r]-() DELETE r")

def delete_nodes(session: Session) -> None:
    session.run("MATCH (n) DELETE n")

def clean_database() -> None:
    """Remove all nodes and relationships from the database."""
    driver = GraphDatabase.driver(DATABASE_URI, auth=(AUTH_USERNAME, AUTH_PASSWORD))
    
    with driver.session() as session:
        delete_realtionships(session)
        delete_nodes(session)
        print("Database cleaned successfully.")
    
    driver.close()


if __name__ == "__main__":
    clean_database()
