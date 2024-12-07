from project.gateways.csv_loader import CSVLoader
from pandas import read_csv
import pandas as pd

def test_csv_loader_load_dataset():
    file_path = "tests/gateways/files/test_csv_loader.csv"
    loader = CSVLoader()
    df = loader.load_dataset(file_path)

    expected = pd.DataFrame({"id": [1, 2], "name": ["Kirill", "Tat"]})

    pd.testing.assert_frame_equal(df, expected)

