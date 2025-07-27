""" TESTS FOR DATA PROCESSING MODULE """

from app.services.utils.data_processing import DataProcessor, get_unsaved_operations, date_to_int
from app.database.models import Operation
from datetime import date
from decimal import Decimal
import pytest

import pandas as pd

def test_file_preprocessing(dataframe):
    
    processor = DataProcessor(dataframe)
    processor._preprocess_file()
    
    correct_dataframe = pd.DataFrame(
            data=[
                ["2025-02-23", "ZUS ODDZIAŁ ŁÓDŹ  PRZELEW PRZYCHODZĄCY", "Wpływy stałe", 3500.00, "PLN"],
                ["2025-02-22", "SHELL STACJA PALIW 1234  ZAKUP PRZY UŻYCIU KARTY W KRAJU", "Transport i paliwo", -239.99, "PLN"],
                ["2025-02-21", "ALLEGRO.PL PŁATNOŚĆ BLIK P2P", "Zakupy online", -125.00, "PLN"]
            ],
            columns=["#Data operacji", "#Opis operacji", "#Kategoria", "Kwota", "Waluta"]
        )
    correct_dataframe["#Data operacji"] = pd.to_datetime(correct_dataframe["#Data operacji"])
    
    ## acts like {assert == condition...} without assert keyword
    pd.testing.assert_frame_equal(processor.operations, correct_dataframe) # assert (processor.operations == correct_operations).all().all() #XD?

def test_file_preprocessing_and_category_correction(dataframe):
    processor = DataProcessor(dataframe)
    processor._preprocess_file()
    processor._correct_categories()
    
    correct_dataframe = pd.DataFrame(
            data=[
                ["2025-02-23", "ZUS ODDZIAŁ ŁÓDŹ  PRZELEW PRZYCHODZĄCY", "PRZELEW", 3500.00, "PLN"],
                ["2025-02-22", "SHELL STACJA PALIW 1234  ZAKUP PRZY UŻYCIU KARTY W KRAJU", "Transport i paliwo", -239.99, "PLN"],
                ["2025-02-21", "ALLEGRO.PL PŁATNOŚĆ BLIK P2P", "BLIK", -125.00, "PLN"]
            ],
            columns=["#Data operacji", "#Opis operacji", "#Kategoria", "Kwota", "Waluta"]
        )
    correct_dataframe["#Data operacji"] = pd.to_datetime(correct_dataframe["#Data operacji"])
    
    pd.testing.assert_frame_equal(processor.operations, correct_dataframe) 

def test_get_unsaved_operations_all_in_database(processed_dataframe):
    
    operations_in_database = [
        Operation(
            operation_id=1,
            user_id=2,
            operation_date=date(2025, 2, 23),
            category="PRZELEW",
            description="ZUS ODDZIAŁ ŁÓDŹ  PRZELEW PRZYCHODZĄCY",
            value=Decimal("3500.00"),
            currency="PLN"
        ),
        Operation(
            operation_id=2,
            user_id=2,
            operation_date=date(2025, 2, 22),
            category="Transport i paliwo",
            description="SHELL STACJA PALIW 1234  ZAKUP PRZY UŻYCIU KARTY W KRAJU",
            value=Decimal("-239.99"),
            currency="PLN"
        ),
        Operation(
            operation_id=3,
            user_id=2,
            operation_date=date(2025, 2, 21),
            category="BLIK",
            description="ALLEGRO.PL PŁATNOŚĆ BLIK P2P",
            value=Decimal("-125.00"),
            currency="PLN"
        ),
        Operation(
            operation_id=4,
            user_id=2,
            operation_date=date(2025, 5, 18),
            category="Utilities",
            description="Electricity bill",
            value=Decimal("65.75"),
            currency="USD"
        )] 
    
    operations_to_save = pd.DataFrame(
            data=[],
            columns=["#Data operacji", "#Opis operacji", "#Kategoria", "Kwota", "Waluta"]
        )
    
    operations_to_save["#Data operacji"] = pd.to_datetime(operations_to_save["#Data operacji"])
    operations_to_save["Kwota"] = operations_to_save["Kwota"].astype('float64')
    
    unsaved_operations = get_unsaved_operations(saved_operations=operations_in_database, new_operations=processed_dataframe)
    print("OPERACJE DO ZAPISDAFAFAF\n" ,operations_to_save.shape)
    print("OPERACJE NIEZAPISANE\n" ,unsaved_operations.shape)
    assert unsaved_operations.shape == operations_to_save.shape

    pd.testing.assert_frame_equal(
        get_unsaved_operations(saved_operations=operations_in_database, new_operations=processed_dataframe),
        operations_to_save                                   
        )   
    
def test_get_unsaved_operations_partially_in_database(processed_dataframe):

    operations_in_database = [
        Operation(
            operation_id=1,
            user_id=2,
            operation_date=date(2025, 2, 23),
            category="PRZELEW",
            description="ZUS ODDZIAŁ ŁÓDŹ  PRZELEW PRZYCHODZĄCY",
            value=Decimal("3500.00"),
            currency="PLN"
        ),
        Operation(
            operation_id=2,
            user_id=2,
            operation_date=date(2025, 2, 22),
            category="Transport i paliwo",
            description="SHELL STACJA PALIW 1234  ZAKUP PRZY UŻYCIU KARTY W KRAJU",
            value=Decimal("-239.99"),
            currency="PLN"
        )] 
    
    operations_to_save = pd.DataFrame(
            data=[
                    ["2025-02-21", "ALLEGRO.PL PŁATNOŚĆ BLIK P2P", "BLIK", -125.00, "PLN"]
                  ],
            columns=["#Data operacji", "#Opis operacji", "#Kategoria", "Kwota", "Waluta"]
        )
    operations_to_save["#Data operacji"] = pd.to_datetime(operations_to_save["#Data operacji"])
    

    pd.testing.assert_frame_equal(
        get_unsaved_operations(saved_operations=operations_in_database, new_operations=processed_dataframe).reset_index(drop=True),
        operations_to_save,                               
        )  

def test_get_unsaved_operations_none_in_database(processed_dataframe):
    
    operations_in_database = []

    operations_to_save = pd.DataFrame(
            data=[
                ["2025-02-23", "ZUS ODDZIAŁ ŁÓDŹ  PRZELEW PRZYCHODZĄCY", "PRZELEW", 3500.00, "PLN"],
                ["2025-02-22", "SHELL STACJA PALIW 1234  ZAKUP PRZY UŻYCIU KARTY W KRAJU", "Transport i paliwo", -239.99, "PLN"],
                ["2025-02-21", "ALLEGRO.PL PŁATNOŚĆ BLIK P2P", "BLIK", -125.00, "PLN"]
                  ],
            columns=["#Data operacji", "#Opis operacji", "#Kategoria", "Kwota", "Waluta"]
        )
    operations_to_save["#Data operacji"] = pd.to_datetime(operations_to_save["#Data operacji"])

    pd.testing.assert_frame_equal(
        get_unsaved_operations(saved_operations=operations_in_database, new_operations=processed_dataframe),
        operations_to_save                                   
        )   
    

def test_date_to_int(operations):
    
    data = [[0.0, -125.0], [1.0, -239.99], [2.0, 3500.00]]
    
    assert date_to_int(operations) == data
    