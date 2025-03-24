from pymongo import MongoClient

mongo_client = None 

def get_mongo_client():
    global mongo_client
    if mongo_client is None:
        mongo_client = MongoClient("mongodb://localhost:27017/")
    return mongo_client
