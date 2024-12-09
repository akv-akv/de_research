import pytest
import pandas as pd
from unittest.mock import MagicMock
from project.gateways.case_loader import CaseLoader
from project.domain.query import Query

@pytest.fixture
def mock_yaml_loader():
    return MagicMock()

@pytest.fixture
def case_loader(mock_yaml_loader):
    return CaseLoader(yaml_loader=mock_yaml_loader)


@pytest.fixture
def query_dir_setup(tmp_path):
    def _setup(query_sql=None, datasets=None, expected_results=None, config=None):
        query_dir = tmp_path / "query_1"
        query_dir.mkdir()

        # Create query.sql file
        if query_sql:
            (query_dir / "query.sql").write_text(query_sql)

        # Create test_cases directory
        test_suite_dir = query_dir / "test_cases" / "suite_1"
        test_suite_dir.mkdir(parents=True)

        # Create dataset files
        if datasets:
            for table_name, data in datasets.items():
                pd.DataFrame(data).to_csv(test_suite_dir / f"{table_name}.csv", index=False)

        # Create expected results file
        if expected_results:
            pd.DataFrame(expected_results).to_csv(test_suite_dir / "expected_results_query.csv", index=False)

        # Use default config if none is provided
        default_config = {
            "test_suites": {
                "suite_1": {
                    "datasets": {table: f"{table}.csv" for table in datasets} if datasets else {},
                    "expected_results": {"query": "expected_results_query.csv"},
                }
            }
        }
        config = config or default_config

        # Create config.yaml
        import yaml
        with open(query_dir / "config.yaml", "w") as f:
            yaml.dump(config, f)

        return query_dir, config

    return _setup


def test_load_test_case_success(case_loader, query_dir_setup, mock_yaml_loader):
    datasets = {"users": {"id": [1], "name": ["Alice"]}}
    expected_results = {"id": [1], "name": ["Alice"]}
    query_dir, config = query_dir_setup(
        query_sql="SELECT * FROM users",
        datasets=datasets,
        expected_results=expected_results,
    )
    mock_yaml_loader.load_dict_from_yaml.return_value = config

    query, datasets, expected_result = case_loader.load_test_case(query_dir, "suite_1")

    assert query == Query(name="root_query", sql_code="SELECT * FROM users")
    pd.testing.assert_frame_equal(datasets["users"], pd.DataFrame({"id": [1], "name": ["Alice"]}))
    pd.testing.assert_frame_equal(expected_result, pd.DataFrame({"id": [1], "name": ["Alice"]}))


@pytest.mark.parametrize(
    "missing_key, expected_exception, match",
    [
        ("test_suites", KeyError, "'test_suites' not found or malformed"),
        ("suite_1", KeyError, "Test suite 'suite_1' not found"),
    ],
)
def test_load_test_case_invalid_config(case_loader, query_dir_setup, mock_yaml_loader, missing_key, expected_exception, match):
    query_dir, _ = query_dir_setup()
    invalid_config = {"invalid_key": {}} if missing_key == "test_suites" else {"test_suites": {}}
    mock_yaml_loader.load_dict_from_yaml.return_value = invalid_config

    with pytest.raises(expected_exception, match=match):
        case_loader.load_test_case(query_dir, "suite_1")

@pytest.mark.parametrize(
    "missing_key, missing_file, expected_exception, match",
    [
        ("datasets", "missing_users.csv", FileNotFoundError, "missing_users.csv"),
        ("expected_results", "missing_results.csv", FileNotFoundError, "missing_results.csv"),
    ],
)
def test_load_test_case_missing_files(
    case_loader, query_dir_setup, mock_yaml_loader, missing_key, missing_file, expected_exception, match
):
    datasets = {"users": {"id": [1], "name": ["Alice"]}}
    query_dir, config = query_dir_setup(
        query_sql="SELECT * FROM users",
        datasets=datasets,
        expected_results={"id": [1], "name": ["Alice"]},
    )

    # Modify config to create missing files scenario
    if missing_key == "datasets":
        config["test_suites"]["suite_1"]["datasets"] = {"users": missing_file}
    elif missing_key == "expected_results":
        config["test_suites"]["suite_1"]["expected_results"]["query"] = missing_file

    mock_yaml_loader.load_dict_from_yaml.return_value = config

    with pytest.raises(expected_exception, match=match):
        case_loader.load_test_case(query_dir, "suite_1")
