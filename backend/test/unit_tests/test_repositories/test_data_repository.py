import pytest
from app.database.repositories import DataRepository
from app.database.models import Operation
from datetime import date
from decimal import Decimal
from app.database.exceptions import ParameterError

def test_get_user_operations(session):
    
    data_repository = DataRepository(session_factory=session)
    
    # with pytest.raises(TypeError):
        
    #     data_repository.get_user_operations(user_id="3")
    
    # no user_id
    with pytest.raises(TypeError):
        data_repository.get_user_operations()
        
    # typo in order
    with pytest.raises(ParameterError):  
        data_repository.get_user_operations(user_id=2, order="aasc")
        
    # typo in operation_type
    with pytest.raises(ParameterError):
        data_repository.get_user_operations(user_id=2, operation_type="spending")
    
    # wrong group_by
    with pytest.raises(ParameterError):
        data_repository.get_user_operations(user_id=2, group_by="user_id")
    
    # user_id
    operation_list = [
        Operation(
            operation_id=4,
            user_id=2,
            operation_date=date(2025, 5, 18),
            category="Utilities",
            description="Electricity bill",
            value=Decimal("-65.75"),
            currency="USD"
        ),
        Operation(
            operation_id=5,
            user_id=2,
            operation_date=date(2025, 5, 19),
            category="Dining",
            description="Dinner at Luigi's",
            value=Decimal("-45.00"),
            currency="USD"
        ),
        Operation(
            operation_id=6,
            user_id=2,
            operation_date=date(2025, 5, 22),
            category="Health",
            description="Pharmacy purchase",
            value=Decimal("-22.10"),
            currency="USD"
        )
    ]
    
    for a, b in zip(data_repository.get_user_operations(user_id=2), operation_list):
        assert a.is_equal(b) 
    
    # date_from
    operation_list = [
        Operation(
            operation_id=5,
            user_id=2,
            operation_date=date(2025, 5, 19),
            category="Dining",
            description="Dinner at Luigi's",
            value=Decimal("-45.00"),
            currency="USD"
        ),
        Operation(
            operation_id=6,
            user_id=2,
            operation_date=date(2025, 5, 22),
            category="Health",
            description="Pharmacy purchase",
            value=Decimal("-22.10"),
            currency="USD"
        )
    ]

    for a,b in zip(data_repository.get_user_operations(user_id=2, date_from=date(2025, 5, 19)), operation_list):
        assert a.is_equal(b)

    # date_to
    operation_list = [
         Operation(
            operation_id=4,
            user_id=2,
            operation_date=date(2025, 5, 18),
            category="Utilities",
            description="Electricity bill",
            value=Decimal("-65.75"),
            currency="USD"
        ),
        Operation(
            operation_id=5,
            user_id=2,
            operation_date=date(2025, 5, 19),
            category="Dining",
            description="Dinner at Luigi's",
            value=Decimal("-45.00"),
            currency="USD"
        ),
    ]
    
    for a,b in zip(data_repository.get_user_operations(user_id=2, date_to=date(2025, 5, 19)), operation_list):
        assert a.is_equal(b)
    
    # date_from, date_to
    operation_list = [
        Operation(
            operation_id=5,
            user_id=2,
            operation_date=date(2025, 5, 19),
            category="Dining",
            description="Dinner at Luigi's",
            value=Decimal("-45.00"),
            currency="USD"
        )
    ]
    
    for a,b in zip(data_repository.get_user_operations(user_id=2, date_from=date(2025, 5, 19), date_to=date(2025, 5, 20)), operation_list):
        assert a.is_equal(b)
    
    # order desc
    operation_list = [
        Operation(
            operation_id=6,
            user_id=2,
            operation_date=date(2025, 5, 22),
            category="Health",
            description="Pharmacy purchase",
            value=Decimal("-22.10"),
            currency="USD"
        ),
        Operation(
            operation_id=5,
            user_id=2,
            operation_date=date(2025, 5, 19),
            category="Dining",
            description="Dinner at Luigi's",
            value=Decimal("-45.00"),
            currency="USD"
        ),
        Operation(
            operation_id=4,
            user_id=2,
            operation_date=date(2025, 5, 18),
            category="Utilities",
            description="Electricity bill",
            value=Decimal("-65.75"),
            currency="USD"
        )
    ]
    
    for a,b in zip(data_repository.get_user_operations(user_id=2, order="desc"), operation_list):
        assert a.is_equal(b)
    
    # operation_type = spendings
    operation_list = [
        Operation(
            operation_id=4,
            user_id=2,
            operation_date=date(2025, 5, 18),
            category="Utilities",
            description="Electricity bill",
            value=Decimal("-65.75"),
            currency="USD"
        ),
        Operation(
            operation_id=5,
            user_id=2,
            operation_date=date(2025, 5, 19),
            category="Dining",
            description="Dinner at Luigi's",
            value=Decimal("-45.00"),
            currency="USD"
        ),
        Operation(
            operation_id=6,
            user_id=2,
            operation_date=date(2025, 5, 22),
            category="Health",
            description="Pharmacy purchase",
            value=Decimal("-22.10"),
            currency="USD"
        )
    ]
    
    for a,b in zip(data_repository.get_user_operations(user_id=2, operation_type="spendings"), operation_list):
        assert a.is_equal(b)
        
    # operation_type = earnings
    operation_list = []
    
    assert data_repository.get_user_operations(user_id=2, operation_type="earnings") == operation_list
        