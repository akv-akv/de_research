from project.gateways.base_file_loader import BaseFileLoader
import yaml
from pathlib import Path


class YAMLLoader(BaseFileLoader):
    def load_dict_from_yaml(self, file_path: str | Path) -> dict:
        file_path = self.validate_file_path(file_path)
        with file_path.open('r') as file:
            return yaml.safe_load(file)