class Query:
    def __init__(self, name: str, sql_code: str):
        """
        Represents a parsed query or CTE.

        :param name: Name of the query or CTE.
        :param sql_code: The SQL code for the query or CTE.
        """
        self.name = name
        self.sql_code = sql_code