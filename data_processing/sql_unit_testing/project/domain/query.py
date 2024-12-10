class Query:
    def __init__(self, name: str, sql_code: str):
        """
        Represents a parsed query or CTE.

        :param name: Name of the query or CTE.
        :param sql_code: The SQL code for the query or CTE.
        """
        self.name = name
        self.sql_code = sql_code
    
    def __eq__(self, other):
        if not isinstance(other, Query):
            return False
        return self.name == other.name and self.sql_code.strip() == other.sql_code.strip()