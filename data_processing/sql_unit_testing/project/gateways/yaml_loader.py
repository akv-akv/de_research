from project.gateways.base_file_loader import BaseFileLoader
import yaml
from pathlib import Path


class YAMLLoader(BaseFileLoader):
    @classmethod
    def load_dict_from_yaml(self, file_path: str | Path) -> dict:
        file_path = self.validate_file_path(file_path)

        with open(file_path, "r") as file:
            config = yaml.safe_load(file)
            #print(f"Loaded YAML Config: {config}")  # Debugging
        return config