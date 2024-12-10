import pytest
from unittest.mock import MagicMock, patch
from project.use_cases.suite_executor import SuiteExecutor
from project.domain.query import Query
import pandas as pd


@pytest.fixture
def mock_query_engine():
    return MagicMock()


@pytest.fixture
def mock_case_loader():
    return MagicMock()


@pytest.fixture
def suite_executor(mock_query_engine, mock_case_loader):
    return SuiteExecutor(query_engine=mock_query_engine, case_loader=mock_case_loader)


@pytest.mark.parametrize(
    "query_dir, suite_name, query, datasets, expected_result, execute_query_return, expected_validation",
    [
        (
            "queries/1",
            "suite_1",
            Query(name="root_query", sql_code="SELECT * FROM users"),
            {"users": pd.DataFrame({"id": [1], "name": ["Alice"]})},
            pd.DataFrame({"id": [1], "name": ["Alice"]}),
            pd.DataFrame({"id": [1], "name": ["Alice"]}),
            {"success": True, "message": "Validation passed: All checks succeeded."},
        ),
        (
            "queries/1",
            "suite_2",
            Query(name="root_query", sql_code="SELECT * FROM orders"),
            {"orders": pd.DataFrame({"id": [1], "amount": [100]})},
            pd.DataFrame({"id": [1], "amount": [100]}),
            pd.DataFrame({"id": [1], "amount": [100]}),
            {"success": True, "message": "Validation passed: All checks succeeded."},
        ),
    ],
)
@patch("project.use_cases.suite_executor.execute_query_use_case")
def test_execute_single_suite(
    mock_execute_query,
    suite_executor,
    mock_case_loader,
    query_dir,
    suite_name,
    query,
    datasets,
    expected_result,
    execute_query_return,
    expected_validation,
):
    # Arrange
    mock_case_loader.load_test_case.return_value = (query, datasets, expected_result)
    mock_execute_query.return_value = execute_query_return

    # Act
    result = suite_executor.execute_test_suite(query_dir, suite_name)

    # Assert
    mock_case_loader.load_test_case.assert_called_once_with(query_dir, suite_name)
    mock_execute_query.assert_called_once_with(suite_executor.query_engine, query, datasets)
    assert result == expected_validation


@pytest.mark.parametrize(
    "query_dir, config, suite_results",
    [
        (
            "queries/1",
            {"test_suites": {"suite_1": {}, "suite_2": {}}},
            {
                "suite_1": {"success": True, "message": "Validation passed: All checks succeeded."},
                "suite_2": {"success": True, "message": "Validation passed: All checks succeeded."},
            },
        ),
    ],
)
@patch("project.use_cases.suite_executor.execute_query_use_case")
def test_execute_all_suites(
    mock_execute_query,
    suite_executor,
    mock_case_loader,
    query_dir,
    config,
    suite_results,
):
    # Arrange
    query = Query(name="root_query", sql_code="SELECT * FROM users")
    datasets = {"users": pd.DataFrame({"id": [1], "name": ["Alice"]})}
    expected_result = pd.DataFrame({"id": [1], "name": ["Alice"]})
    mock_case_loader.yaml_loader.load_dict_from_yaml.return_value = config
    mock_case_loader.load_test_case.return_value = (query, datasets, expected_result)
    mock_execute_query.return_value = expected_result

    # Act
    results = suite_executor.execute_all_suites(query_dir)

    # Assert
    assert results == suite_results
    assert mock_case_loader.load_test_case.call_count == len(config["test_suites"])
    assert mock_execute_query.call_count == len(config["test_suites"])


@pytest.mark.parametrize(
    "suite_name, exception_type, exception_message",
    [
        ("invalid_suite", KeyError, "Test suite not found"),
    ],
)
def test_execute_suite_invalid_name(
    suite_executor, mock_case_loader, suite_name, exception_type, exception_message
):
    # Arrange
    query_dir = "queries/1"
    mock_case_loader.load_test_case.side_effect = exception_type(exception_message)

    # Act & Assert
    with pytest.raises(exception_type, match=exception_message):
        suite_executor.execute_test_suite(query_dir, suite_name)


@pytest.mark.parametrize(
    "config, expected_results",
    [
        ({"test_suites": {}}, {}),
    ],
)
def test_execute_all_suites_no_suites(
    suite_executor, mock_case_loader, config, expected_results
):
    # Arrange
    query_dir = "queries/1"
    mock_case_loader.load_dict_from_yaml.return_value = config

    # Act
    results = suite_executor.execute_all_suites(query_dir)

    # Assert
    assert results == expected_results
