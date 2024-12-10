from abc import ABC, abstractmethod
from project.domain.query import Query


class SQLParser(ABC):
    # @abstractmethod
    # def extract_tables(self, query: str) -> list[str]:
    #     """Extracts table names from a SQL query."""
    #     pass

    @abstractmethod
    def extract_ctes(self, query: str) -> list[Query]:
        """Extracts CTEs from a SQL query."""
        pass