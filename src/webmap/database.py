imp
import pymongo

def init_db():
    clint = pymongo.MongoClient("mongodb://database:27017/")
    db = clint["webmap"]
    return db

def init_website_collection(db):
    col = db["websites"]
    return col
