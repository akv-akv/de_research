import pytest

class _TestConfig:
    def __init__(self, query_file, test_suites):
        self.query_file = query_file
        self.test_suites = [_TestSuite(**suite) for suite in test_suites]

class _TestSuite:
    def __init__(self, name, tests):
        self.name = name
        self.tests = [_TestCase(**test) for test in tests]

class _TestCase:
    def __init__(self, scope, inputs, expected_results, cte_name=None):
        self.scope = scope
        self.inputs = [TableInput(**input_data) for input_data in inputs]
        self.expected_results = expected_results
        self.cte_name = cte_name

class TableInput:
    def __init__(self, table_name, file_path):
        self.table_name = table_name
        self.file_path = file_path