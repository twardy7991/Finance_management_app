from app.services.utils.data_processing import DataProcessor
from app.database.models import Operation

import pytest
import pandas as pd
from pathlib import Path
from datetime import date
from decimal import Decimal

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

@pytest.fixture
def operations():
    return [
        Operation(
            operation_id=3,
            user_id=2,
            operation_date=date(2025, 2, 21),
            category="BLIK",
            description="ALLEGRO.PL PŁATNOŚĆ BLIK P2P",
            value=Decimal(-125.00),
            currency="PLN"
        ),
        Operation(
            operation_id=2,
            user_id=2,
            operation_date=date(2025, 2, 22),
            category="Transport i paliwo",
            description="SHELL STACJA PALIW 1234  ZAKUP PRZY UŻYCIU KARTY W KRAJU",
            value=Decimal(-239.99),
            currency="PLN"
        ),
        Operation(
            operation_id=1,
            user_id=2,
            operation_date=date(2025, 2, 23),
            category="PRZELEW",
            description="ZUS ODDZIAŁ ŁÓDŹ  PRZELEW PRZYCHODZĄCY",
            value=Decimal(3500.00),
            currency="PLN"
        )
    ]