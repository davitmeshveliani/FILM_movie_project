from pymongo import MongoClient
from pymongo.database import Database
from config import MONGO_URI, MONGO_DB_NAME
from typing import Any

def initialize_database() -> None:
    """
    Initializes the database by creating TTL (Time-To-Live) indexes
    for automatic cleanup of old logs and search history
    """
    try:
        client: Any = MongoClient(MONGO_URI)
        db: Database = client[MONGO_DB_NAME]

        db["search_history"].create_index([("timestamp", 1)], expireAfterSeconds=2592000)
        db["error_logs"].create_index([("timestamp", 1)], expireAfterSeconds=7776000)

        print("TTL indexes created successfully in MongoDB Atlas.")
    except Exception as e:
        print(f"Error creating indexes: {e}")
# if __name__ == "__main__":
#     initialize_database()