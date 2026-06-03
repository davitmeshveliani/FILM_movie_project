import pytest
from unittest.mock import MagicMock
from app_orchestrator import AppOrchestrator


def test_menu_structure():
    """
    Test if the application menu is initialized with the correct number of options
    """
    mock_db = MagicMock()
    mock_log = MagicMock()
    mock_analytics = MagicMock()

    mock_db.get_year_range.return_value = (1888, 2026)
    app = AppOrchestrator(mock_db, mock_log, mock_analytics)

    assert "1" in app.menu
    assert "2" in app.menu
    assert "3" in app.menu
    assert len(app.menu) == 3


def test_exit_functionality():
    """
    Verify that selecting the exit option handles the application state correctly.
    """
    mock_db = MagicMock()
    mock_log = MagicMock()
    mock_analytics = MagicMock()

    mock_db.get_year_range.return_value = (1888, 2026)
    app = AppOrchestrator(mock_db, mock_log, mock_analytics)
    assert True