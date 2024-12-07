from project.gateways.sqlglot_parser import SQLGlotParser

def test_sqlglot_parser_extract_tables():
    # Arrange
    query = "SELECT id, name FROM users JOIN orders ON users.id = orders.user_id"
    parser = SQLGlotParser()

    # Act
    tables = parser.extract_tables(query)

    # Assert
    assert tables == ["users", "orders"]