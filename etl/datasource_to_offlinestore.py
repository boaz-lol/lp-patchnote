import json
import os

from pymongo import MongoClient
from dotenv import load_dotenv

if __name__ == '__main__':
    uri = os.getenv("MONGO_URI")
    client = MongoClient(uri)

    db = client["lpdb"]
    collection = db["data_source"]

    