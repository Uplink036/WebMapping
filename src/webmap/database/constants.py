import os

from dotenv import load_dotenv

load_dotenv()

DATABASE_URI = os.getenv("NEO4j_URI", "neo4j://localhost")
AUTH_USERNAME = os.getenv("NEO4j_USERNAME", "admin")
AUTH_PASSWORD = os.getenv("NEO4j_PASSWORD", "password")