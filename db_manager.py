from typing import List, Tuple, Any
from mysql.connector import Error
from collections import namedtuple

Movie = namedtuple('Movie', ['title', 'release_year', 'rating', 'length'])

class MovieDatabase:
    """
    Database connector class for managing interactions with the MySQL Sakila database.
    """

    TITLE_SEARCH_QUERY: str = (
        "SELECT title, release_year, rating, length "
        "FROM film "
        "WHERE title LIKE %s "
        "ORDER BY CAST(release_year AS UNSIGNED) ASC, title DESC "
        "LIMIT 10 OFFSET %s"
    )

    GENRE_YEAR_SEARCH_QUERY: str = """
        SELECT f.title, f.release_year, f.rating, f.length 
        FROM film f
        JOIN film_category fc ON f.film_id = fc.film_id
        JOIN category c ON fc.category_id = c.category_id
        WHERE LOWER(c.name) = LOWER(%s) 
          AND f.release_year BETWEEN %s AND %s
          AND f.title IS NOT NULL
        ORDER BY f.release_year ASC, f.title DESC
        LIMIT 10 OFFSET %s
    """

    def __init__(self, cursor: Any) -> None:
        """
        Initializes the database connector with a cursor.

        Args:
            cursor (Any): The MySQL database cursor object for executing queries.
        """
        self.cursor = cursor

    def search_by_title(self, keyword: str, offset: int = 0) -> List[Movie]:
        """
        Searches for movies by title using a keyword and returns a list of Movie namedtuples.

        Args:
            keyword (str): The string to search for in movie titles.
            offset (int): The number of records to skip for pagination.

        Returns:
            List[Movie]: A list of Movie objects matching the keyword

        Raises:
            RuntimeError: If a database error occurs during the search.
        """
        try:
            self.cursor.execute(self.TITLE_SEARCH_QUERY, (f"%{keyword}%", int(offset)))
            return [Movie(*row) for row in self.cursor.fetchall()]
        except Error as e:
            raise RuntimeError(f"Database query error during title search: {e}")

    def get_genres(self) -> List[str]:
        """
        Retrieves all available movie categories from the database.

        Returns:
            List[str]: A list of genre names sorted alphabetically.

        Raises:
            RuntimeError: If a database error occurs during retrieval.
        """
        try:
            self.cursor.execute("SELECT name FROM category ORDER BY name ASC")
            return [str(row[0]) for row in self.cursor.fetchall()]
        except Error as e:
            raise RuntimeError(f"Database error during genre retrieval: {e}")

    def get_year_range(self) -> Tuple[int, int]:
        """
        Retrieves the minimum and maximum release years available in the database.

        Returns:
            Tuple[int, int]: A tuple containing the (min_year, max_year).

        Raises:
            RuntimeError: If a database error occurs during retrieval.
        """
        try:
            self.cursor.execute("SELECT MIN(release_year), MAX(release_year) FROM film")
            res: Any = self.cursor.fetchone()
            if res and res[0]:
                return int(res[0]), int(res[1])
            return 1888, 2026
        except Error as e:
            raise RuntimeError(f"Database error during year range retrieval: {e}")

    def search_by_genre_year(self, genre: str, y_from: int, y_to: int, offset: int = 0) -> List[Movie]:
        """
            Filters movies by a specific category and a release year range.

            Args:
                genre (str): The genre name to filter by.
                y_from (int): The starting year of the range.
                y_to (int): The ending year of the range.
                offset (int): The number of records to skip for pagination.

            Returns:
                List[Movie]: A list of Movie objects matching the filters.

            Raises:
                RuntimeError: If a database error occurs during filtering.
            """
        try:
            self.cursor.execute(
                self.GENRE_YEAR_SEARCH_QUERY,
                (str(genre), int(y_from), int(y_to), int(offset))
            )
            return [Movie(*row) for row in self.cursor.fetchall()]
        except Error as e:
            raise RuntimeError(f"Database error during genre and year filtering. Detail: {e}")