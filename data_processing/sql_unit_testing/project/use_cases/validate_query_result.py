import pandas as pd

class ValidateQueryResultUseCase:
    @staticmethod
    def validate(actual_result, expected_result):
        """
        Validate if the actual query result matches the expected result.

        :param actual_result: A pandas DataFrame of the actual query result.
        :param expected_result: A pandas DataFrame of the expected result.
        :return: A dictionary with 'success' (bool) and 'message' (str).
        """
        # Compare column names
        column_comparison = ValidateQueryResultUseCase._compare_columns(actual_result, expected_result)
        if not column_comparison["success"]:
            return column_comparison

        # Compare DataFrame size
        size_comparison = ValidateQueryResultUseCase._compare_dataframe_size(actual_result, expected_result)
        if not size_comparison["success"]:
            return size_comparison

        # Compare DataFrame content
        content_comparison = ValidateQueryResultUseCase._compare_dataframe_content(actual_result, expected_result)
        if not content_comparison["success"]:
            return content_comparison

        # If all comparisons pass
        return {"success": True, "message": "Validation passed: All checks succeeded."}

    @staticmethod
    def _compare_columns(actual_result, expected_result):
        """Compare column names between actual and expected DataFrames."""
        actual_columns = list(actual_result.columns)
        expected_columns = list(expected_result.columns)
        if actual_columns != expected_columns:
            return {
                "success": False,
                "message": (
                    "Column Comparison Failed:\n"
                    f"  - Expected Columns: {expected_columns}\n"
                    f"  - Actual Columns:   {actual_columns}"
                ),
            }
        return {"success": True}

    @staticmethod
    def _compare_dataframe_size(actual_result, expected_result):
        """Compare the number of rows between actual and expected DataFrames."""
        actual_row_count = len(actual_result)
        expected_row_count = len(expected_result)
        if actual_row_count != expected_row_count:
            return {
                "success": False,
                "message": (
                    "Row Count Comparison Failed:\n"
                    f"  - Expected Rows: {expected_row_count}\n"
                    f"  - Actual Rows:   {actual_row_count}"
                ),
            }
        return {"success": True}

    @staticmethod
    def _compare_dataframe_content(actual_result, expected_result):
        """Compare the content of actual and expected DataFrames with detailed feedback."""
        try:
            # Assert that the DataFrames are equal, allowing for column order differences
            pd.testing.assert_frame_equal(actual_result, expected_result, check_like=True)
        except AssertionError as e:
            # Collect detailed differences for better error reporting
            differences = []
            
            # Check for column differences
            if list(actual_result.columns) != list(expected_result.columns):
                differences.append(
                    f"Column Mismatch:\n"
                    f"  - Expected Columns: {list(expected_result.columns)}\n"
                    f"  - Actual Columns:   {list(actual_result.columns)}"
                )

            # Check for shape differences
            if actual_result.shape != expected_result.shape:
                differences.append(
                    f"Shape Mismatch:\n"
                    f"  - Expected Shape: {expected_result.shape}\n"
                    f"  - Actual Shape:   {actual_result.shape}"
                )

            # Compare cell-level differences using a mask
            diff_mask = (actual_result != expected_result) & ~(actual_result.isna() & expected_result.isna())
            differing_rows_actual = actual_result[diff_mask.any(axis=1)]
            differing_rows_expected = expected_result[diff_mask.any(axis=1)]
            if not differing_rows_actual.empty:
                differences.append(
                    f"Data Differences actual\n(First 5 mismatched rows):\n{differing_rows_actual.head(5)}\n"
                    f"Data Differences expected\n(First 5 mismatched rows):\n{differing_rows_expected.head(5)}"
                )
            
            # Combine all difference details
            detailed_message = "\n".join(differences) or str(e)

            return {
                "success": False,
                "message": (
                    "Data Comparison Failed:\n"
                    f"{detailed_message}"
                ),
            }

        # If no errors, return success
        return {"success": True}