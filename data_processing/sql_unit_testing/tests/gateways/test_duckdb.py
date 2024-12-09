import pytest
import pandas as pd
from pathlib import Path
from project.gateways.duckdb_database import DuckdbGateway

@pytest.fixture
def duckdb_gateway():
    """Fixture to provide a fresh instance of DuckdbGateway for each test."""
    return DuckdbGateway(db_path=":memory:")

def test_register_table(duckdb_gateway):
    df = pd.DataFrame({"id": [1, 2], "name": ["Alice", "Bob"]})
    duckdb_gateway.register_table("users", df)
    result = duckdb_gateway.execute_query("SELECT * FROM users")

    pd.testing.assert_frame_equal(result, df)

def test_execute_query(duckdb_gateway):
    # Arrange: Create and populate a table directly in DuckDB
    duckdb_gateway.connection.execute("""
        CREATE TABLE orders (order_id INTEGER, amount FLOAT);
        INSERT INTO orders VALUES (1, 100.0), (2, 150.0);
    """)

    # Act: Execute a query
    result = duckdb_gateway.execute_query("SELECT SUM(amount) as total FROM orders")

    # Assert: Verify the aggregated result
    expected = pd.DataFrame({"total": [250.0]})
    pd.testing.assert_frame_equal(result, expected)
