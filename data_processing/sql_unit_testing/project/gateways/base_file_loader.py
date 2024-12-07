from pathlib import Path

class BaseFileLoader:
    @staticmethod
    def validate_file_path(file_path: str | Path) -> Path:
        """
        Validates and converts a file path to a Path object.

        :param file_path: The file path to validate.
        :return: A validated Path object.
        :raises FileNotFoundError: If the file does not exist.
        """
        path = Path(file_path).resolve()
        if not path.is_file():
            raise FileNotFoundError(f"File not found: {path}")
        return path