from project.domain.query import Query

def test_query_initialization():
    query = Query(
        name="cte1",
        sql_code="SELECT * FROM table1",
    )

    assert query.name == "cte1"
    assert query.sql_code == "SELECT * FROM table1"
