from app.services.data_processing import DataProcessor
import pytest
import pandas as pd
from pathlib import Path

filepath = Path(__file__).parent

@pytest.fixture
def dataframe():
    return pd.read_csv(f"{filepath}/data/lista_operacji_small.csv", skiprows=25, sep=";")

@pytest.fixture
def processed_dataframe(dataframe):
    processor = DataProcessor(dataframe)
    processor._preprocess_file()
    processor._correct_categories()
    return processor.operations