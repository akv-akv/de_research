from typing import Dict
import pandas as pd
from project.domain.query import Query
from project.gateways.database import DatabaseEngineGateway

def execute_query_use_case(query_engine: DatabaseEngineGateway, query: Query, datasets: Dict[str, pd.DataFrame]) -> pd.DataFrame:
    """
    Executes a SQL query using the provided query engine and datasets.

    :param query_engine: An implementation of DatabaseEngineGateway.
    :param query: The Query object containing the SQL code.
    :param datasets: A dictionary mapping table names to DataFrames.
    :return: A DataFrame containing the query results.
    """
    # Register datasets
    for table_name, data_frame in datasets.items():
        query_engine.register_table(table_name, data_frame)

    # Execute the query
    result = query_engine.execute_query(query.sql_code)

    return result