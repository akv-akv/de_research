import pandas as pd
import pytest
from project.use_cases.validate_query_result import ValidateQueryResultUseCase

@pytest.mark.parametrize(
    "actual, expected, expected_result",
    [
        # Matching results
        (
            pd.DataFrame({"id": [1, 2], "name": ["Alice", "Bob"]}),
            pd.DataFrame({"id": [1, 2], "name": ["Alice", "Bob"]}),
            {"success": True, "message": "Validation passed: All checks succeeded."},
        ),
        # Mismatching results
        (
            pd.DataFrame({"id": [1, 2], "name": ["Alice", "Charlie"]}),
            pd.DataFrame({"id": [1, 2], "name": ["Alice", "Bob"]}),
            {
                "success": False,
                "message_contains": [
                    "Data Comparison Failed",
                    "Differences",
                    "DataFrame.iloc[:, 1] (column name=\"name\") are different",
                    "[left]:  [Alice, Charlie]",
                    "[right]: [Alice, Bob]",
                ],
            },
        ),
        # Empty results
        (
            pd.DataFrame(),
            pd.DataFrame(),
            {"success": True, "message": "Validation passed: All checks succeeded."},
        ),
        # Column mismatch
        (
            pd.DataFrame({"id": [1, 2], "name": ["Alice", "Bob"]}),
            pd.DataFrame({"id": [1, 2], "full_name": ["Alice", "Bob"]}),
            {
                "success": False,
                "message_contains": [
                    "Column Comparison Failed",
                    "Expected Columns: ['id', 'full_name']",
                    "Actual Columns:   ['id', 'name']",
                ],
            },
        ),
        # Row mismatch
        (
            pd.DataFrame({"id": [1], "name": ["Alice"]}),
            pd.DataFrame({"id": [1, 2], "name": ["Alice", "Bob"]}),
            {
                "success": False,
                "message_contains": [
                    "Row Count Comparison Failed",
                    "Expected Rows: 2",
                    "Actual Rows:   1",
                ],
            },
        ),
    ],
)
def test_validate_query_result_use_case(actual, expected, expected_result):
    result = ValidateQueryResultUseCase.validate(actual, expected)
    
    # Assert success flag matches
    assert result["success"] == expected_result["success"]
    
    # Assert exact match for message when provided
    if "message" in expected_result:
        assert result["message"] == expected_result["message"]
    # Assert message contains key phrases for dynamic messages
    elif "message_contains" in expected_result:
        for phrase in expected_result["message_contains"]:
            assert phrase in result["message"]
