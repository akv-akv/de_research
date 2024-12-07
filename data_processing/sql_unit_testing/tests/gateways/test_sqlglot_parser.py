from project.gateways.sqlglot_parser import SQLGlotParser

import pytest

@pytest.mark.parametrize(
    "query, expected_tables",
    [
        # Simple SELECT
        ("SELECT id, name FROM users", ["users"]),
        # JOIN queries
        ("SELECT id, name FROM users JOIN orders ON users.id = orders.user_id", ["users", "orders"]),
        ("SELECT id FROM customers INNER JOIN invoices ON customers.id = invoices.customer_id", ["customers", "invoices"]),
        ("SELECT * FROM employees LEFT JOIN departments ON employees.department_id = departments.id", ["employees", "departments"]),
        ("SELECT * FROM sales FULL OUTER JOIN refunds ON sales.id = refunds.sale_id", ["sales", "refunds"]),
        # Nested queries
        ("SELECT * FROM (SELECT id FROM products) AS subquery", ["products"]),
        # Subqueries
        ("SELECT id FROM (SELECT user_id FROM logs) log_sub", ["logs"]),
        # Case sensitivity
        ("SELECT * FROM USERS", ["USERS"]),
        ("SELECT * FROM \"Users\"", ["Users"]),
        # Aliases
        ("SELECT u.id FROM users AS u", ["users"]),
        # Reserved keywords as table names
        ("SELECT * FROM \"select\"", ["select"]),
        # Cross join
        ("SELECT * FROM a CROSS JOIN b", ["a", "b"]),
        # Multiple joins
        (
            "SELECT * FROM a JOIN b ON a.id = b.id JOIN c ON b.id = c.id",
            ["a", "b", "c"],
        ),
        # Complex queries
        (
            "SELECT id FROM (SELECT * FROM table1 JOIN table2 ON table1.id = table2.id) AS subquery",
            ["table1", "table2"],
        ),
        # UNION
        ("SELECT id FROM table1 UNION SELECT id FROM table2", ["table1", "table2"]),
        # No table
        ("SELECT 1", []),
        # CTE query
        (
            "WITH recent_orders AS (SELECT * FROM orders WHERE order_date > '2023-01-01') "
            "SELECT * FROM recent_orders JOIN users ON recent_orders.user_id = users.id",
            ["orders", "users"],
        ),
        # Complex table name with schema and database
        (
            "SELECT id, name FROM db_name.schema_name.table_name",
            ["table_name"],
        ),
        # Complex table name with special characters
        (
            "SELECT * FROM \"schema-name\".\"table-name\"",
            ["table-name"],
        ),
    ],
)
def test_sqlglot_parser_extract_tables(query, expected_tables):
    # Arrange
    parser = SQLGlotParser()

    # Act
    tables = parser.extract_tables(query)

    # Assert
    assert tables == expected_tables
