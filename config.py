import os
from typing import Dict, Any, Final
from dotenv import load_dotenv

ENV_FILE: Final[str] = ".env"

DEFAULT_ENV: Final[str] = """
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=
MYSQL_DATABASE=sakila

MONGO_URI=
MONGO_DB_NAME=movies_db
MONGO_COLLECTION_NAME=movies
"""

def setup_env() -> None:
    """
    Checks for the existence of the .env file.
    If it does not exist, it creates one using the DEFAULT_ENV template.
    """
    if not os.path.exists(ENV_FILE):
        with open(ENV_FILE, "w", encoding="utf-8") as f:
            f.write(DEFAULT_ENV.strip())
        print(f"[INFO] {ENV_FILE} file created automatically.")

setup_env()
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