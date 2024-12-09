from project.gateways.base_file_loader import BaseFileLoader
from project.gateways.dataset_loader import DatasetLoader
import pandas as pd
from pathlib import Path

class CSVLoader(BaseFileLoader, DatasetLoader):
    @classmethod
    def load_dataset(self, file_path: str | Path) -> pd.DataFrame:
        file_path = self.validate_file_path(file_path)
        return pd.read_csv(file_path)
