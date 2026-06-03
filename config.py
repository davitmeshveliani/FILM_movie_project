import os
from typing import Dict, Any, Final
from dotenv import load_dotenv

load_dotenv()

def get_env_variable(key: str) -> str:
    """
        Retrieves an environment variable by key.
        Args:
            key: The name of the environment variable.
        Returns:
            The value of the environment variable as a string.
        Raises:
            ValueError: If the environment variable is not set
        """
    value = os.getenv(key)
    if not value:
        raise ValueError(f"Environment variable '{key}' is not set!")
    return value

MYSQL_CONFIG: Final[Dict[str, Any]] = {
    'host': get_env_variable('MYSQL_HOST'),
    'user': get_env_variable('MYSQL_USER'),
    'password': get_env_variable('MYSQL_PASSWORD'),
    'database': get_env_variable('MYSQL_DATABASE'),
    'port': int(os.getenv('MYSQL_PORT', 3306))
}

MONGO_URI: Final[str] = get_env_variable('MONGO_URI')
MONGO_DB_NAME: Final[str] = get_env_variable('MONGO_DB_NAME')
MONGO_COLLECTION_NAME: Final[str] = get_env_variable('MONGO_COLLECTION_NAME')