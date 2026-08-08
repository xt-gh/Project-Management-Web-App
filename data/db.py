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
    # Use 5 seconds timeout for cloud database connection
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000, tlsCAFile=certifi.where())
    db = client["projectDatabase"]
    # Quick connectivity check
    client.server_info()
    print("\033[32m[INFO] Successfully connected to MongoDB Atlas Cloud!\033[0m")
except Exception as e:
    print(f"\033[31m[ERROR] Failed to connect to MongoDB Atlas: {e}\033[0m")
    
    # Only fall back to local MongoDB if we are NOT running in the cloud (Render/Docker)
    if not os.getenv("PORT"):
        print("[INFO] Falling back to local MongoDB at localhost:27017")
        try:
            client = MongoClient("mongodb://localhost:27017/", serverSelectionTimeoutMS=2000, tlsCAFile=certifi.where())
            db = client["projectDatabase"]
            client.server_info()
        except Exception as local_err:
            print(f"[ERROR] Local MongoDB fallback failed: {local_err}")
            db = None
    else:
        # In cloud environments, do not fall back to localhost
        db = None
