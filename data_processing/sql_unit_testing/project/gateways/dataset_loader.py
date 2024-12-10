from abc import ABC, abstractmethod
from pathlib import Path
import pandas as pd

class DatasetLoader(ABC):
    @abstractmethod
    def load_dataset(self, file_path: str | Path) -> pd.DataFrame:
        """
        Loads a dataset into a Pandas DataFrame.

        :param file_path: Path to the dataset file.
        :return: Pandas DataFrame containing the dataset.
        """
        pass