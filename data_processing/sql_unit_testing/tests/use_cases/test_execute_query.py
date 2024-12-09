from unittest.mock import MagicMock
import pandas as pd
import pytest
from project.use_cases.execute_query import execute_query_use_case
from project.domain.query import Query
from project.gateways.duckdb_database import DuckdbGateway


# Unit tests
@pytest.fixture
def mock_query_engine():
    """Fixture for a mocked query engine."""
    return MagicMock()

def test_execute_query_registers_tables(mock_query_engine):
    # Arrange
    query = Query(name="test_query", sql_code="SELECT * FROM users")
    datasets = {"users": pd.DataFrame({"id": [1, 2], "name": ["Alice", "Bob"]})}
    mock_query_engine.execute_query.return_value = datasets["users"]

    # Act
    result = execute_query_use_case(mock_query_engine, query, datasets)

    # Assert
    mock_query_engine.register_table.assert_called_once_with("users", datasets["users"])
    mock_query_engine.execute_query.assert_called_once_with(query.sql_code)
    pd.testing.assert_frame_equal(result, datasets["users"])

def test_execute_query_executes_sql(mock_query_engine):
    # Arrange
    query = Query(name="test_query", sql_code="SELECT name FROM users WHERE id = 1")
    datasets = {"users": pd.DataFrame({"id": [1, 2], "name": ["Alice", "Bob"]})}
    expected_result = pd.DataFrame({"name": ["Alice"]})
    mock_query_engine.execute_query.return_value = expected_result

    # Act
    result = execute_query_use_case(mock_query_engine, query, datasets)

    # Assert
    mock_query_engine.execute_query.assert_called_once_with(query.sql_code)
    pd.testing.assert_frame_equal(result, expected_result)

def test_execute_query_handles_multiple_tables(mock_query_engine):
    # Arrange
    query = Query(name="join_query", sql_code="SELECT * FROM users JOIN orders ON users.id = orders.user_id")
    datasets = {
        "users": pd.DataFrame({"id": [1, 2], "name": ["Alice", "Bob"]}),
        "orders": pd.DataFrame({"order_id": [101, 102], "user_id": [1, 2], "amount": [50.0, 75.0]}),
    }
    expected_result = pd.DataFrame({
        "id": [1, 2],
        "name": ["Alice", "Bob"],
        "order_id": [101, 102],
        "user_id": [1, 2],
        "amount": [50.0, 75.0],
    })
    mock_query_engine.execute_query.return_value = expected_result

    # Act
    result = execute_query_use_case(mock_query_engine, query, datasets)

    # Assert
    mock_query_engine.register_table.assert_any_call("users", datasets["users"])
    mock_query_engine.register_table.assert_any_call("orders", datasets["orders"])
    pd.testing.assert_frame_equal(result, expected_result)


# Integration tests
@pytest.mark.parametrize(
    "query, datasets, expected_result",
    [
        # Basic query
        (
            Query(name="basic_query", sql_code="SELECT * FROM users"),
            {"users": pd.DataFrame({"id": [1, 2], "name": ["Alice", "Bob"], "age": [30, 25]})},
            pd.DataFrame({"id": [1, 2], "name": ["Alice", "Bob"], "age": [30, 25]}),
        ),
        # Query with WHERE clause
        (
            Query(name="filter_query", sql_code="SELECT id, name FROM users WHERE age > 25"),
            {"users": pd.DataFrame({"id": [1, 2, 3], "name": ["Alice", "Bob", "Charlie"], "age": [30, 25, 35]})},
            pd.DataFrame({"id": [1, 3], "name": ["Alice", "Charlie"]}),
        ),
        # Query with JOIN
        (
            Query(name="join_query", sql_code="SELECT users.id, users.name, orders.amount FROM users JOIN orders ON users.id = orders.user_id"),
            {
                "users": pd.DataFrame({"id": [1, 2], "name": ["Alice", "Bob"]}),
                "orders": pd.DataFrame({"order_id": [101, 102], "user_id": [1, 2], "amount": [50.0, 75.0]}),
            },
            pd.DataFrame({"id": [1, 2], "name": ["Alice", "Bob"], "amount": [50.0, 75.0]}),
        ),
        # Query with schema
        (
            Query(name="schema_query", sql_code='SELECT * FROM "public.users"'),
            {"public.users": pd.DataFrame({"id": [1, 3], "name": ["Alice", "Charlie"], "age": [30, 35]})},
            pd.DataFrame({"id": [1, 3], "name": ["Alice", "Charlie"], "age": [30, 35]}),
        ),
        # Query with quoted table
        (
            Query(name="quoted_query", sql_code='SELECT * FROM "users"'),
            {"users": pd.DataFrame({"id": [1], "name": ["Alice"], "age": [30]})},
            pd.DataFrame({"id": [1], "name": ["Alice"], "age": [30]}),
        ),
    ],
)
def test_execute_query_integration(query, datasets, expected_result):
    # Arrange
    query_engine = DuckdbGateway(db_path=":memory:")

    # Act
    result = execute_query_use_case(query_engine, query, datasets)

    # Assert
    pd.testing.assert_frame_equal(result, expected_result)