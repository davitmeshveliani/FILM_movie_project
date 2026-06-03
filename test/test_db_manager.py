import pytest
from unittest.mock import MagicMock
from db_manager import MovieDatabase, Movie


def test_search_by_title():
    """
    Test that search_by_title executes the query correctly and parses the result
    """
    mock_cursor = MagicMock()
    mock_cursor.fetchall.return_value = [("Titanic", 1997, "PG-13", 194)]
    db = MovieDatabase(mock_cursor)
    results = db.search_by_title("Titanic")

    assert len(results) == 1
    assert results[0].title == "Titanic"
    assert results[0].release_year == 1997
    assert mock_cursor.execute.called


def test_get_genres():
    """
    Test that get_genres retrieves and formats the list correctly.
    """
    mock_cursor = MagicMock()
    mock_cursor.fetchall.return_value = [("Action",), ("Comedy",)]

    db = MovieDatabase(mock_cursor)
    genres = db.get_genres()

    assert "Action" in genres
    assert "Comedy" in genres
    assert len(genres) == 2