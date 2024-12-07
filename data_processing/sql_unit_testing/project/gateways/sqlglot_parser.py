from sqlglot import parse_one, exp
from project.gateways.sql_parser import SQLParser


class SQLGlotParser(SQLParser):
    def extract_tables(self, query: str) -> list[str]:
        """Extract table names using sqlglot."""
        ast = parse_one(query)
        return [table.name for table in ast.find_all(exp.Table)]