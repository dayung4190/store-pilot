import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

mongo_uri = os.getenv("MONGO_URI")

client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)

db_name = os.getenv("DB_NAME", "store_pilot")
db = client[db_name]

products_collection = db["products"]