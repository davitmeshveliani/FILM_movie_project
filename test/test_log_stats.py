import pytest
from unittest.mock import MagicMock
from log_stats import SearchAnalytics


def test_get_popular_searches():
    """
    Test that the SearchAnalytics correctly processes aggregation results
    """
    mock_db = MagicMock()

    mock_db["search_history"].aggregate.return_value = [
        {"_id": "Titanic", "count": 10},
        {"_id": "Action", "count": 5}
    ]

    analytics = SearchAnalytics(mock_db)
    results = analytics.get_popular_searches(limit=5)

    assert len(results) == 2
    assert results[0].keyword == "Titanic"
    assert results[0].count == 10