# from project.gateways.sqlglot_parser import QueryParserGateway
from project.gateways.sqlglot_parser import SQLGlotParser
from project.domain.query import Query

import pytest

# @pytest.mark.parametrize(
#     "query, expected_tables",
#     [
#         # Simple SELECT
#         ("SELECT id, name FROM users", ["users"]),
#         # JOIN queries
#         ("SELECT id, name FROM users JOIN orders ON users.id = orders.user_id", ["users", "orders"]),
#         ("SELECT id FROM customers INNER JOIN invoices ON customers.id = invoices.customer_id", ["customers", "invoices"]),
#         ("SELECT * FROM employees LEFT JOIN departments ON employees.department_id = departments.id", ["employees", "departments"]),
#         ("SELECT * FROM sales FULL OUTER JOIN refunds ON sales.id = refunds.sale_id", ["sales", "refunds"]),
#         # Nested queries
#         ("SELECT * FROM (SELECT id FROM products) AS subquery", ["products"]),
#         # Subqueries
#         ("SELECT id FROM (SELECT user_id FROM logs) log_sub", ["logs"]),
#         # Case sensitivity
#         ("SELECT * FROM USERS", ["USERS"]),
#         ("SELECT * FROM \"Users\"", ["Users"]),
#         # Aliases
#         ("SELECT u.id FROM users AS u", ["users"]),
#         # Reserved keywords as table names
#         ("SELECT * FROM \"select\"", ["select"]),
#         # Cross join
#         ("SELECT * FROM a CROSS JOIN b", ["a", "b"]),
#         # Multiple joins
#         (
#             "SELECT * FROM a JOIN b ON a.id = b.id JOIN c ON b.id = c.id",
#             ["a", "b", "c"],
#         ),
#         # Complex queries
#         (
#             "SELECT id FROM (SELECT * FROM table1 JOIN table2 ON table1.id = table2.id) AS subquery",
#             ["table1", "table2"],
#         ),
#         # UNION
#         ("SELECT id FROM table1 UNION SELECT id FROM table2", ["table1", "table2"]),
#         # No table
#         ("SELECT 1", []),
#         # CTE query
#         (
#             "WITH recent_orders AS (SELECT * FROM orders WHERE order_date > '2023-01-01') "
#             "SELECT * FROM recent_orders JOIN users ON recent_orders.user_id = users.id",
#             ["orders", "users"],
#         ),
#         # Complex table name with schema and database
#         (
#             "SELECT id, name FROM db_name.schema_name.table_name",
#             ["table_name"],
#         ),
#         # Complex table name with special characters
#         (
#             "SELECT * FROM \"schema-name\".\"table-name\"",
#             ["table-name"],
#         ),
#     ],
# )
# def test_sqlglot_parser_extract_tables(query, expected_tables):
#     # Arrange
#     parser = SQLGlotParser()

#     # Act
#     tables = parser.extract_tables(query)

#     # Assert
#     assert tables == expected_tables


@pytest.mark.parametrize(
    "query, expected_ctes",
    [
        # Case 1: No CTEs, simple query
        ("SELECT 1", []),

        # Case 2: Multiple CTEs with no nesting
        (
            """WITH cte1 AS (SELECT * FROM table1), cte2 AS (SELECT * FROM cte1 WHERE col > 10) SELECT * FROM cte2;""",
            {
                "cte1": Query(name="cte1", sql_code="SELECT * FROM table1"),
                "cte2": Query(name="cte2", sql_code="SELECT * FROM cte1 WHERE col > 10"),
            },
        ),

        # Case 3: Single CTE with no dependencies
        (
            """WITH cte1 AS (SELECT col1, col2 FROM table2) SELECT * FROM cte1;""",
            {
                "cte1": Query(name="cte1", sql_code="SELECT col1, col2 FROM table2"),
            },
        ),

        # Case 4: CTEs with joins
        (
            """WITH cte1 AS (SELECT a.id, b.name FROM table1 a JOIN table2 b ON a.id = b.id) SELECT * FROM cte1;""",
            {
                "cte1": Query(name="cte1", sql_code="SELECT a.id, b.name FROM table1 AS a JOIN table2 AS b ON a.id = b.id"),
            },
        ),

        # Case 5: Invalid SQL (should return empty list)
        ("INVALID QUERY", []),
    ],
)
def test_query_parser_extract_ctes(query, expected_ctes):
    parser = SQLGlotParser()
    ctes = parser.extract_ctes(query)

    assert len(ctes) == len(expected_ctes)
    if len(ctes) > 0:
        for cte in ctes:
            expected_cte = expected_ctes[cte.name]
            assert cte.name == expected_cte.name
            assert cte.sql_code.strip() == expected_cte.sql_code.strip()