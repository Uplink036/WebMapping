import pymongo

def init_db():
    clint = pymongo.MongoClient("mongodb://database:27017/")
    db = clint["webmap"]
    return db

def init_node_collection(db):
    col = db["nodes"]
    return col

def init_edge_collection(db):
    col = db["edges"]
    return col
