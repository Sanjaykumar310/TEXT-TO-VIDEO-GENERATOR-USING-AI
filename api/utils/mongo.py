from pymongo import MongoClient
import os
from gridfs import GridFS

def get_mongo_client():
    MONGO_URI = os.environ.get("MONGO_URI")
    return MongoClient(MONGO_URI)

def get_db(db_name="text_to_video_db"):
    return get_mongo_client()[db_name]

def get_collection(db_name, collection_name):
    client = get_mongo_client()
    return client[db_name][collection_name]

def get_gridfs_bucket(db_name="text_to_video_db"):
    db = get_db(db_name)
    return GridFS(db)
