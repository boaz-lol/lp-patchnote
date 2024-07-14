import os
import requests
from datetime import datetime

from pymongo import MongoClient
from dotenv import load_dotenv

MONGODB_DATABASE_URL = os.getenv("MONGO_URI")

def get_db():
    client = MongoClient(MONGODB_DATABASE_URL)
    db =  client["lpdb"]
    return db