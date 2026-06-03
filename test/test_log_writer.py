import pytest
from unittest.mock import MagicMock
from log_writer import MongoLogger


def test_log_search():
    """
    Test that the MongoLogger correctly calls the insert method on the database
    """
    mock_db = MagicMock()
    logger = MongoLogger()
    logger.db = mock_db
    logger.save_search_log("Title", {"title": "Titanic"}, 1)
    assert mock_db["search_history"].insert_one.called