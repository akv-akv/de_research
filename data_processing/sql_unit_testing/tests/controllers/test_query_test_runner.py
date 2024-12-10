import pytest
from pathlib import Path
from unittest.mock import MagicMock, patch
from project.controllers.query_test_runner import QueryTestRunner

@pytest.fixture
def mock_executor():
    return MagicMock()

@pytest.fixture
def runner(mock_executor):
    with patch("project.controllers.query_test_runner.SuiteExecutor", return_value=mock_executor):
        yield QueryTestRunner()

def test_run_test_suite_success(runner, mock_executor, tmp_path):
    # Arrange
    query_dir = tmp_path / "queries" / "1"
    test_suite = "suite_1"
    mock_executor.execute_test_suite.return_value = {"success": True, "message": "Validation passed."}

    # Act
    runner.run_test_suite(query_dir, test_suite)

    # Assert
    mock_executor.execute_test_suite.assert_called_once_with(query_dir, test_suite)

def test_run_test_suite_failure(runner, mock_executor, tmp_path):
    # Arrange
    query_dir = tmp_path / "queries" / "1"
    test_suite = "suite_1"
    mock_executor.execute_test_suite.return_value = {"success": False, "message": "Validation failed."}

    # Act
    runner.run_test_suite(query_dir, test_suite)

    # Assert
    mock_executor.execute_test_suite.assert_called_once_with(query_dir, test_suite)

def test_run_all_suites(runner, mock_executor, tmp_path):
    # Arrange
    query_dir = tmp_path / "queries" / "1"
    mock_executor.execute_all_suites.return_value = {
        "suite_1": {"success": True, "message": "Validation passed."},
        "suite_2": {"success": False, "message": "Validation failed."},
    }

    # Act
    runner.run_all_suites(query_dir)

    # Assert
    mock_executor.execute_all_suites.assert_called_once_with(query_dir)
