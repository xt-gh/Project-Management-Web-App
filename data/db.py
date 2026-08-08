import os
import sys
import certifi
from pymongo import MongoClient

# Fetch MongoDB URI from environment, or default to a fallback.
# User can customize this URI as needed.
MONGO_URI = os.getenv(
    "MONGO_URI",
    "mongodb+srv://wxt132_db_user:Wxt_0067@cluster0.akd9qgr.mongodb.net/"
)

# Print a warning if the placeholder URI is still present
if "helium.xxxx.mongodb.net" in MONGO_URI:
    print("\033[33m[WARNING] Please configure your MONGO_URI in the environment or edit data/db.py with your connection string.\033[0m")

client = None
db = None

try:
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=2000, tlsCAFile=certifi.where())
    db = client["projectDatabase"]
    # Quick connectivity check
    client.server_info()
except Exception as e:
    print(f"\033[31m[ERROR] Failed to connect to MongoDB: {e}\033[0m")
    # If connection/DNS resolution failed, fallback to a local MongoDB client
    # so that the imports do not crash on start-up.
    try:
        client = MongoClient("mongodb://localhost:27017/", serverSelectionTimeoutMS=2000, tlsCAFile=certifi.where())
        db = client["projectDatabase"]
    except Exception:
        db = None
