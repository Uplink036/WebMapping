from webmap.database.constants import AUTH_PASSWORD, AUTH_USERNAME, DATABASE_URI 
from neo4j import GraphDatabase

def verify_connectivity():
    with GraphDatabase.driver(DATABASE_URI, auth=(AUTH_USERNAME, AUTH_PASSWORD)) as driver:
        try:
            driver.verify_connectivity()
            return True
        except Exception as e:
            print("Database error:", e)
            return False

if __name__ == "__main__":
    if verify_connectivity():
        print("Successful database connection")