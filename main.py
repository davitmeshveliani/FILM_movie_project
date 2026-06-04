from mysql.connector import connect, Error
from config import MYSQL_CONFIG
from db_manager import MovieDatabase
from log_writer import MongoLogger
from log_stats import SearchAnalytics
from app_orchestrator import AppOrchestrator


def main() -> None:
    """
        Main entry point of the application.

        Establishes a connection to the MySQL database, initializes the necessary
        logging and analytics modules, and orchestrates the application execution.
        Ensures that database resources are properly closed after execution.
        """

    conn = None
    cur = None

    try:
        conn = connect(**MYSQL_CONFIG)
        cur = conn.cursor()

        with MongoLogger() as log:
            db = MovieDatabase(cur)
            analytics = SearchAnalytics(log.db)
            app = AppOrchestrator(db, log, analytics)
            app.run()

    except Error as e:
        print(f"Connection failed: {e}")

    finally:
        if cur is not None:
            cur.close()
        if conn and conn.is_connected():
            conn.close()


if __name__ == "__main__":
    main()