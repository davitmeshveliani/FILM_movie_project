from mysql.connector import connect, Error
from mysql.connector.cursor import MySQLCursor
from mysql.connector.connection import MySQLConnection
from config import MYSQL_CONFIG
from db_manager import MovieDatabase
from log_writer import MongoLogger
from log_stats import SearchAnalytics
from app_orchestrator import AppOrchestrator


def main() -> None:
    """
    The main entry point of the application.

    Initializes database connections (MySQL and MongoDB), sets up dependencies,
    and starts the application orchestrator. Ensures proper resource cleanup
    """
    conn = None
    try:
        conn = connect(**MYSQL_CONFIG)
        cur: MySQLCursor = conn.cursor()

        with MongoLogger() as log:
            db = MovieDatabase(cur)
            analytics = SearchAnalytics(log.db)
            app = AppOrchestrator(db, log, analytics)
            app.run()

    except Error as e:
        print(f"Connection failed: {e}")

    finally:
        if conn and conn.is_connected():
            cur.close()
            conn.close()


if __name__ == "__main__":
    main()