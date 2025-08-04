import pytest
from app.database.models import Operation
from sqlalchemy import select
from app.database.utils.utils import stmt_parser, data_frame_to_operation_list
from datetime import date
from sqlalchemy.dialects import sqlite
from app.database.exceptions import UserNotProvidedError
import pandas as pd
from decimal import Decimal

def test_parser_all_params():
    
    stmt = select(Operation).where(
            Operation.user_id == 2,
            Operation.operation_date >= date(2024, 10, 10),  
            Operation.operation_date <= date(2024, 10, 10),
            Operation.value < 0
        ).order_by(
            Operation.operation_date.desc()
        ).group_by(
            Operation.category
        )
    
    assert stmt_parser(user_id=2,
                       date_from=date(2024, 10, 10),
                       date_to=date(2024, 10, 10),
                       order="desc",
                       operation_type="spendings",
                       group_by="category").compare(stmt)
    
def test_one_param_missing():
    
    # user_id missing
    with pytest.raises(TypeError):
        
        stmt = stmt_parser(date_from=date(2024, 10, 10),
                date_to=date(2024, 10, 10),
                order="asc",
                operation_type="spendings",
                group_by="category")
    
    # date_from missing
    stmt = select(Operation).where(
            Operation.user_id == 2,
            Operation.operation_date <= date(2024, 10, 10),
            Operation.value < 0
        ).order_by(
            Operation.operation_date.asc()
        ).group_by(
            Operation.category
        )
    
    assert stmt_parser(user_id=2,
                       date_to=date(2024, 10, 10),
                       order="asc",
                       operation_type="spendings",
                       group_by="category").compare(stmt)
    
    # date_to missing
    stmt = select(Operation).where(
            Operation.user_id == 2,
            Operation.operation_date >= date(2024, 10, 10), 
            Operation.value < 0
        ).order_by(
            Operation.operation_date.asc()
        ).group_by(
            Operation.category
        )
    
    assert stmt_parser(user_id=2,
                       date_from=date(2024, 10, 10),
                       order="asc",
                       operation_type="spendings",
                       group_by="category").compare(stmt)
    
    # order missing
    stmt = select(Operation).where(
            Operation.user_id == 2,
            Operation.operation_date >= date(2024, 10, 10), 
            Operation.operation_date <= date(2024, 10, 10),
            Operation.value < 0
        ).order_by(
            Operation.operation_date.asc()
        ).group_by(
            Operation.category
        )
    
    assert stmt_parser(user_id=2,
                       date_from=date(2024, 10, 10),
                       date_to=date(2024, 10, 10),
                       operation_type="spendings",
                       group_by="category").compare(stmt)
    
    # operation_type missing
    stmt = select(Operation).where(
            Operation.user_id == 2,
            Operation.operation_date >= date(2024, 10, 10), 
            Operation.operation_date <= date(2024, 10, 10),
        ).order_by(
            Operation.operation_date.asc()
        ).group_by(
            Operation.category
        )
    
    assert stmt_parser(user_id=2,
                       date_from=date(2024, 10, 10),
                       date_to=date(2024, 10, 10),
                       order="asc",
                       group_by="category").compare(stmt)
    
    # group_by missing
    stmt = select(Operation).where(
            Operation.user_id == 2,
            Operation.operation_date >= date(2024, 10, 10), 
            Operation.operation_date <= date(2024, 10, 10),
            Operation.value < 0
        ).order_by(
            Operation.operation_date.asc()
        )
    
    assert stmt_parser(user_id=2,
                       date_from=date(2024, 10, 10),
                       date_to=date(2024, 10, 10),
                       order="asc",
                       operation_type="spendings"
                       ).compare(stmt)

def test_df_to_operation_list():

    data_file = pd.DataFrame(data=[
            [date(2025, 2, 21),
            "BLIK",
            "ALLEGRO.PL PŁATNOŚĆ BLIK P2P",
            Decimal(-125.00),
            "PLN"
            ],
            [date(2025, 2, 22),
            "Transport i paliwo",
            "SHELL STACJA PALIW 1234  ZAKUP PRZY UŻYCIU KARTY W KRAJU",
            Decimal(-239.99),
            "PLN"
            ],
            [date(2025, 2, 23),
            "PRZELEW",
            "ZUS ODDZIAŁ ŁÓDŹ  PRZELEW PRZYCHODZĄCY",
            Decimal(3500.00),
            "PLN"
            ] 
        ],
        columns=["#Data operacji", 
                 "#Kategoria", 
                 "#Opis operacji", 
                 "Kwota", 
                 "Waluta"])
    
    operation_list = [
        Operation(
            user_id=2,
            operation_date=date(2025, 2, 21),
            category="BLIK",
            description="ALLEGRO.PL PŁATNOŚĆ BLIK P2P",
            value=Decimal(-125.00),
            currency="PLN"
        ),
        Operation(
            user_id=2,
            operation_date=date(2025, 2, 22),
            category="Transport i paliwo",
            description="SHELL STACJA PALIW 1234  ZAKUP PRZY UŻYCIU KARTY W KRAJU",
            value=Decimal(-239.99),
            currency="PLN"
        ),
        Operation(
            user_id=2,
            operation_date=date(2025, 2, 23),
            category="PRZELEW",
            description="ZUS ODDZIAŁ ŁÓDŹ  PRZELEW PRZYCHODZĄCY",
            value=Decimal(3500.00),
            currency="PLN"
        )
    ]
    
    for a, b in zip(data_frame_to_operation_list(user_id=2, data_file=data_file), operation_list):
        assert a.is_equal(b)
    
    
    
    
    