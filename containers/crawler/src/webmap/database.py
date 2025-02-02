import pymongo
import os
from dotenv import load_dotenv

load_dotenv()

def init_db():
    clint = pymongo.MongoClient("mongodb://database:27017/")
    db = clint["webmap"]
    scrub_db = os.getenv('SCRUB_DB')
    if int(scrub_db) == 1:
        clint.drop_database("webmap")
        db = clint["webmap"]
    return db

def init_node_collection(db):
    col = db["nodes"]
    return col

def init_edge_collection(db):
    col = db["edges"]
    return col
