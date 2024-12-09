import duckdb
import pandas as pd
from project.gateways.database import DatabaseEngineGateway

class DuckdbGateway(DatabaseEngineGateway):
    def __init__(self, db_path: str = ":memory:"):
        """
        Initializes the DuckDB connection.

        :param db_path: Path to the DuckDB database (defaults to in-memory).
        """
        self.connection = duckdb.connect(db_path)

    def register_table(self, table_name: str, data_frame: pd.DataFrame):
        """
        Registers a Pandas DataFrame as a table in DuckDB.

        :param table_name: Name of the table.
        :param data_frame: Pandas DataFrame to register as a table.
        """
        self.connection.register(table_name, data_frame)

    def execute_query(self, sql: str) -> pd.DataFrame:
        """
        Executes a SQL query in DuckDB.

        :param sql: The SQL query to execute.
        :return: Query results as a Pandas DataFrame.
        """
        return self.connection.execute(sql).fetchdf()
