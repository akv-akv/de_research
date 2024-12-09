import typer
from pathlib import Path
from project.controllers.query_test_runner import QueryTestRunner

app = typer.Typer(help="SQL Query Test Runner")

@app.command()
def run_tests(
    query_dir: str = typer.Argument(
        ...,  # This makes it a required positional argument
        help="Path to the query directory (e.g., queries/1)"
    ),
    test_suite: str = typer.Option(
        None,
        "--test-suite",
        "-t",
        help="Name of the test suite to run. If omitted, all suites will be executed."
    ),
):
    """
    Runs tests for SQL queries against input datasets and validates results.
    """
    query_runner = QueryTestRunner()

    if test_suite:
        query_runner.run_test_suite(query_dir, test_suite)
    else:
        query_runner.run_all_suites(query_dir)



if __name__ == "__main__":
    app()