from unittest.mock import MagicMock, patch

import pytest


@pytest.fixture
def mock_neo4j():
    """Mock neo4j GraphDatabase and related components for testing."""

    # Mock record object
    mock_record = MagicMock()
    mock_record.__getitem__ = MagicMock(return_value="test_value")
    mock_record.get = MagicMock(return_value="test_value")

    # Mock result object
    mock_result = MagicMock()
    mock_result.single.return_value = mock_record
    mock_result.data.return_value = [{"test": "data"}]

    # Mock session object
    mock_session = MagicMock()
    mock_session.run.return_value = mock_result
    mock_session.__enter__ = MagicMock(return_value=mock_session)
    mock_session.__exit__ = MagicMock(return_value=None)

    # Mock driver object
    mock_driver = MagicMock()
    mock_driver.session.return_value = mock_session
    mock_driver.verify_connectivity.return_value = None
    mock_driver.__enter__ = MagicMock(return_value=mock_driver)
    mock_driver.__exit__ = MagicMock(return_value=None)

    # Mock GraphDatabase
    mock_graph_database = MagicMock()
    mock_graph_database.driver.return_value = mock_driver

    with patch("neo4j.GraphDatabase", mock_graph_database):
        with patch("webmap.database.connection.GraphDatabase", mock_graph_database):
            with patch("webmap.database.database.GraphDatabase", mock_graph_database):
                yield {
                    "driver": mock_driver,
                    "session": mock_session,
                    "result": mock_result,
                    "record": mock_record,
                    "graph_database": mock_graph_database,
                }
