from abc import ABC, abstractmethod
import pandas as pd

class DatabaseEngineGateway(ABC):
    @abstractmethod
    def register_table(self, table_name: str, df: pd.DataFrame):
        """Registers a dataset as a table."""
        pass

    @abstractmethod
    def execute_query(self, sql: str) -> pd.DataFrame:
        """Executes a SQL query and returns the results as a DataFrame."""
        pass
