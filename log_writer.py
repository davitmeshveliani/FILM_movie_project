from config import MONGO_URI, MONGO_DB_NAME
from datetime import datetime
from typing import Dict, Any, Optional
from pymongo import MongoClient
from pymongo.database import Database
from dotenv import load_dotenv

load_dotenv()


class MongoLogger:
    """
    Handles centralized connection management and structured logging to MongoDB.
    Uses the context manager pattern (__enter__, __exit__) for resource cleanup
    """

    def __init__(self) -> None:
        """Initializes the MongoLogger with configuration from environment variables."""
        self.uri = MONGO_URI
        self.db_name = MONGO_DB_NAME
        self.client: Optional[MongoClient] = None
        self.db: Optional[Database] = None

    def __enter__(self) -> 'MongoLogger':
        """Establishes connection to the MongoDB server."""
        self.client = MongoClient(self.uri)
        self.db = self.client[self.db_name]
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Closes the MongoDB connection."""
        if self.client:
            self.client.close()

    def error(self, message: str, file_name: str = "main.py") -> None:
        """
        Logs an error message to the 'error_logs' collection.
        Args:
            message: The error description.
            file_name: The file name where the error occurred.
        """
        if self.db is None:
            return

        try:
            log_data: Dict[str, Any] = {
                                        "timestamp": datetime.now(),
                                        "level": "ERROR",
                                        "message": message,
                                        "file": file_name
                                        }
            self.db["error_logs"].insert_one(log_data)
        except Exception as e:
            print(f"Logging failed: {e}")

    def save_search_log(self, search_type: str, criteria: Dict[str, Any], results_count: int) -> None:
        """
        Logs a successful search operation to the 'search_history' collection.
        Args:
            search_type: The category of search performed.
            criteria: Search parameters dictionary.
            results_count: Number of results returned.
        """
        if self.db is None:
            return

        try:
            log_data: Dict[str, Any] = {
                                        "timestamp": datetime.now(),
                                        "search_type": search_type,
                                        "criteria": criteria,
                                        "results_count": results_count
                                         }
            self.db["search_history"].insert_one(log_data)
        except Exception as e:
            print(f"Search logging failed: {e}")