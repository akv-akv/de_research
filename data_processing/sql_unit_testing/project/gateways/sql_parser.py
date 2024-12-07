from abc import ABC, abstractmethod


class SQLParser(ABC):
    @abstractmethod
    def extract_tables(self, query: str) -> list[str]:
        """Extracts table names from a SQL query."""
        pass