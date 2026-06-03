import os
from typing import Dict, Any, Final
from dotenv import load_dotenv

"""
SUMMARY:
This module acts as the centralized configuration gateway. It loads sensitive 
environment variables from a .env file and maps them into typed constants 
(MYSQL_CONFIG and MongoDB strings). This approach keeps configuration logic 
separate from application logic, ensures type safety with 'Final', and provides 
default fallback values to maintain application stability.
"""
load_dotenv()

MYSQL_CONFIG: Final[Dict[str, Any]] = {
                            'host': os.getenv('MYSQL_HOST', 'localhost'),
                            'user': os.getenv('MYSQL_USER', 'root'),
                            'password': os.getenv('MYSQL_PASSWORD', ''),
                            'database': os.getenv('MYSQL_DATABASE', 'movies_db'),
                            'port': int(os.getenv('MYSQL_PORT', 3306))
                                     }

MONGO_URI: Final[str] = os.getenv('MONGO_URI', '')
MONGO_DB_NAME: Final[str] = os.getenv('MONGO_DB_NAME', 'movies_db')
MONGO_COLLECTION_NAME: Final[str] = os.getenv('MONGO_COLLECTION_NAME', 'movies')