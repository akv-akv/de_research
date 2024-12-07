from sqlglot import parse_one, exp
from sqlglot.optimizer.scope import build_scope, ScopeType
from project.gateways.sql_parser import SQLParser

from sqlglot.expressions import Table, With
from project.domain.query import Query


class SQLGlotParser(SQLParser):
    # def extract_tables(self, query: str) -> list[Table]:
    #     """Extract table names using sqlglot."""
    #     ast = parse_one(query)
    
    #     root = build_scope(ast)
    #     tables = [
    #         source.name

    #         # Traverse the Scope tree, not the AST
    #         for scope in root.traverse()

    #         # `selected_sources` contains sources that have been selected in this scope, e.g. in a FROM or JOIN clause.
    #         # `alias` is the name of this source in this particular scope.
    #         # `node` is the AST node instancenex
    #         # if the selected source is a subquery (including common table expressions),
    #         #     then `source` will be the Scope instance for that subquery.
    #         # if the selected source is a table,
    #         #     then `source` will be a Table instance.
    #         for alias, (node, source) in scope.selected_sources.items()
    #         if isinstance(source, exp.Table)
    #     ]
    #     return tables

    def extract_ctes(self, query: str) -> list[Query]:
        """
        Extracts CTEs from the given SQL code using Sqlglot.

        :param sql_code: The SQL query to parse.
        :return: A dictionary of Query objects for each CTE.
        """
        ast = parse_one(query)
        ctes = []
        with_clause = ast.find(With)

        if not with_clause:
            return ctes

        all_ctes = with_clause.args['expressions']
        for cte in all_ctes:
            cte_name = cte.find(exp.TableAlias).text('this')
            cte_sql = cte.find(exp.CTE).args['this'].sql()

            ctes.append(Query(name=cte_name, sql_code=cte_sql))

        return ctes
