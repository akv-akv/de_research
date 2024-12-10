import pytest

from project.domain.config import _TestConfig, _TestSuite, _TestCase, TableInput

def test_table_input_initialization():
    # Arrange
    table_name = "users"
    file_path = "path/to/users.csv"

    # Act
    table_input = TableInput(table_name=table_name, file_path=file_path)

    # Assert
    assert table_input.table_name == table_name
    assert table_input.file_path == file_path


def test_test_case_initialization():
    # Arrange
    scope = "query_scope"
    inputs = [
        {"table_name": "users", "file_path": "path/to/users.csv"},
        {"table_name": "orders", "file_path": "path/to/orders.csv"}
    ]
    expected_results = "expected_result_path.csv"
    cte_name = "users_cte"

    # Act
    test_case = _TestCase(scope=scope, inputs=inputs, expected_results=expected_results, cte_name=cte_name)

    # Assert
    assert test_case.scope == scope
    assert len(test_case.inputs) == 2
    assert test_case.inputs[0].table_name == "users"
    assert test_case.inputs[0].file_path == "path/to/users.csv"
    assert test_case.expected_results == expected_results
    assert test_case.cte_name == cte_name


def test_test_suite_initialization():
    # Arrange
    name = "User Tests"
    tests = [
        {
            "scope": "query_scope_1",
            "inputs": [{"table_name": "users", "file_path": "path/to/users.csv"}],
            "expected_results": "expected_result_1.csv",
            "cte_name": "users_cte"
        },
        {
            "scope": "query_scope_2",
            "inputs": [{"table_name": "orders", "file_path": "path/to/orders.csv"}],
            "expected_results": "expected_result_2.csv"
        }
    ]

    # Act
    test_suite = _TestSuite(name=name, tests=tests)

    # Assert
    assert test_suite.name == name
    assert len(test_suite.tests) == 2
    assert test_suite.tests[0].scope == "query_scope_1"
    assert test_suite.tests[0].inputs[0].table_name == "users"
    assert test_suite.tests[1].expected_results == "expected_result_2.csv"


def test_test_config_initialization():
    # Arrange
    query_file = "query.sql"
    test_suites = [
        {
            "name": "Suite 1",
            "tests": [
                {
                    "scope": "scope_1",
                    "inputs": [{"table_name": "users", "file_path": "path/to/users.csv"}],
                    "expected_results": "result_1.csv"
                }
            ]
        },
        {
            "name": "Suite 2",
            "tests": [
                {
                    "scope": "scope_2",
                    "inputs": [{"table_name": "orders", "file_path": "path/to/orders.csv"}],
                    "expected_results": "result_2.csv"
                }
            ]
        }
    ]

    # Act
    test_config = _TestConfig(query_file=query_file, test_suites=test_suites)

    # Assert
    assert test_config.query_file == query_file
    assert len(test_config.test_suites) == 2
    assert test_config.test_suites[0].name == "Suite 1"
    assert test_config.test_suites[0].tests[0].scope == "scope_1"
    assert test_config.test_suites[1].tests[0].inputs[0].table_name == "orders"