from pathlib import Path
from project.gateways.case_loader import CaseLoader
from project.gateways.yaml_loader import YAMLLoader
from project.gateways.duckdb_database import DuckdbGateway
from project.use_cases.suite_executor import SuiteExecutor
import traceback

class QueryTestRunner:
    def __init__(self):
        """
        Initialize the QueryTestRunner with necessary dependencies.
        """
        yaml_loader = YAMLLoader()
        self.case_loader = CaseLoader(yaml_loader=yaml_loader)
        self.query_engine = DuckdbGateway(db_path=":memory:")
        self.executor = SuiteExecutor(query_engine=self.query_engine, case_loader=self.case_loader)

    def run_test_suite(self, query_dir: Path, test_suite: str):
        """
        Runs a single test suite and prints the result with detailed error information.
        """
        try:
            print(f"Running test suite: '{test_suite}' in directory: {query_dir}")
            result = self.executor.execute_test_suite(query_dir, test_suite)
            self._print_result(test_suite, result)
        except Exception as e:
            print(f"Error running test suite '{test_suite}': {e}")
            print("Traceback:")
            traceback.print_exc()

    def run_all_suites(self, query_dir: Path):
        """
        Runs all test suites and prints results for each suite with detailed error information.
        """
        try:
            print(f"Running all test suites in directory: {query_dir}")
            results = self.executor.execute_all_suites(query_dir)
            if not results:
                print(f"No test suites found in configuration for directory: {query_dir}")
                return

            for suite, result in results.items():
                self._print_result(suite, result)
        except Exception as e:
            print(f"Error running all test suites in directory '{query_dir}': {e}")
            print("Traceback:")
            traceback.print_exc()

    def _print_result(self, suite_name: str, result: dict):
        """
        Prints the result of a test suite in a formatted manner.
        """
        status = "PASS" if result.get("success", False) else "FAIL"
        message = result.get("message", "No details available")
        print(f"Test Suite: '{suite_name}' - Status: {status}")
        print(f"Details: {message}")