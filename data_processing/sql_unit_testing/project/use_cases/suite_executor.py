from project.use_cases.validate_query_result import ValidateQueryResultUseCase
from project.use_cases.execute_query import execute_query_use_case
from pathlib import Path
import traceback

class SuiteExecutor:
    def __init__(self, query_engine, case_loader):
        self.query_engine = query_engine
        self.case_loader = case_loader

    def execute_test_suite(self, query_dir, suite_name):
        """
        Execute a single test suite.

        :param query_dir: The directory containing the query and test cases.
        :param suite_name: The name of the test suite to execute.
        :return: A dictionary with 'success' (bool) and 'message' (str).
        """
        # Load the test case
        query, datasets, expected_result = self.case_loader.load_test_case(query_dir, suite_name)

        # Execute the query
        actual_result = execute_query_use_case(self.query_engine ,query, datasets)

        # Validate results
        return ValidateQueryResultUseCase.validate(actual_result, expected_result)

    def execute_all_suites(self, query_dir):
        """
        Execute all test suites in the given query directory.

        :param query_dir: The directory containing the query and test cases.
        :return: A dictionary with test suite names as keys and validation results as values.
        """
        # Load configuration
        config = self.case_loader.yaml_loader.load_dict_from_yaml(Path(query_dir) / "config.yaml")
        test_suites = config.get("test_suites", {})

        results = {}
        for suite_name, suite_details in test_suites.items():
            try:
                # Execute each suite by its name
                results[suite_name] = self.execute_test_suite(query_dir, suite_name)
            except Exception as e:
                # Handle suite execution errors
                results[suite_name] = {
                    "success": False,
                    "message": f"Error executing suite '{suite_name}': {str(e)}",
                    "traceback": traceback.print_exc()
                }

        return results
