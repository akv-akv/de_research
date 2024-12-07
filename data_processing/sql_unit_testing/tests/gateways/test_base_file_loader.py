from project.gateways.base_file_loader import BaseFileLoader
from pathlib import Path
import pytest

@pytest.mark.parametrize(
    "file_input, expect_exception",
    [
        ("files/test.txt", False),                      # Relative string path (valid)
        (Path("files", "test.txt"), False),                # Relative Path object (valid)
        ("nonexistent.txt", True),                # Nonexistent file (string path)
        (Path("nonexistent.txt"), True),          # Nonexistent file (Path object)
        ("./files/test.txt", False),             # Nested relative string path (valid)
        (Path("./files/test.txt"), False),       # Nested relative Path object (valid)
    ],
)
def test_base_file_loader_validate_path(file_input, expect_exception, tmp_path):
    """
    Test the validate_file_path function with both string and Path inputs, and
    dynamically created paths to avoid hardcoded paths.
    """
    if not expect_exception:
        file_path = tmp_path / file_input  # tmp_path ensures isolation
        file_path.parent.mkdir(parents=True, exist_ok=True)  # Create parent directories
        file_path.touch()  # Create an empty file

    # Test the function
    if expect_exception:
        with pytest.raises(FileNotFoundError):
            BaseFileLoader.validate_file_path(tmp_path / file_input)
    else:
        result = BaseFileLoader.validate_file_path(tmp_path / file_input)
        assert result == (tmp_path / file_input).resolve()

