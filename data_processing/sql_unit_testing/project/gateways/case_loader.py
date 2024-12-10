from pathlib import Path
from project.domain.query import Query
from project.gateways.csv_loader import CSVLoader  # Assume this is already implemented


class CaseLoader:
    def __init__(self, yaml_loader, csv_loader=None):
        """
        Initialize the TestCaseLoader.

        :param yaml_loader: An instance of a YAML loader to read the configuration file.
        :param csv_loader: An instance of CSVLoader for loading datasets (default: CSVLoader).
        """
        self.yaml_loader = yaml_loader
        self.csv_loader = csv_loader or CSVLoader()

    def load_test_case(self, query_dir, suite_name):
        config_path = Path(query_dir) / "config.yaml"
        config = self.yaml_loader.load_dict_from_yaml(config_path)
        
        # Ensure 'test_suites' exists and is a dictionary
        if "test_suites" not in config or not isinstance(config["test_suites"], dict):
            raise KeyError(f"'test_suites' not found or malformed in configuration file: {config_path}")
        
        # Ensure the requested suite exists
        if suite_name not in config["test_suites"]:
            raise KeyError(f"Test suite '{suite_name}' not found in configuration.")
        
        suite_config = config["test_suites"][suite_name]

        # Handle missing tests key
        if "tests" not in suite_config or not suite_config["tests"]:
            raise KeyError(f"No tests defined for suite '{suite_name}'.")

        # Parse query and datasets
        query_file = Path(query_dir) / config["query"]["file"]
        if not query_file.exists():
            raise FileNotFoundError(f"Query file '{query_file}' does not exist.")
        
        query = Query(name="root_query", sql_code=query_file.read_text())
        
        datasets = {
            item["table"]: self.csv_loader.load_dataset(Path(query_dir) / item["file"])
            for item in suite_config["tests"][0].get("inputs", [])
        }
        
        # Handle missing expected_results
        if "expected_results" not in suite_config["tests"][0]:
            raise KeyError(f"'expected_results' key missing in suite '{suite_name}' test definition.")
        
        expected_results_path = Path(query_dir) / suite_config["tests"][0]["expected_results"]
        if not expected_results_path.exists():
            raise FileNotFoundError(f"Expected results file '{expected_results_path}' does not exist.")
        
        expected_results = self.csv_loader.load_dataset(expected_results_path)

        return query, datasets, expected_results
