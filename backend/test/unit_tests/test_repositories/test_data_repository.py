import pytest
from app.database.repositories import DataRepository
from app.database.models import Operation, User
from datetime import date
from decimal import Decimal
from app.database.exceptions import ParameterError
from typing import List


    
def test_get_user_operations(data_repository : DataRepository):
    
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
    
def test_get_user_operations_user_id(data_repository : DataRepository):
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

def test_get_user_operations_date_from(data_repository : DataRepository):
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

def test_get_user_operations_date_to(data_repository : DataRepository):
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
    
    
def test_get_user_operations_date_from_date_to(data_repository : DataRepository):
    
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
    
def test_get_user_operations_operation_type_spendings(data_repository : DataRepository):
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
        
def test_get_user_operations_operation_type_earnings(data_repository : DataRepository):
    operation_list = []
    
    assert data_repository.get_user_operations(user_id=2, operation_type="earnings") == operation_list
    
def test_delete_operations_using_objects(data_repository : DataRepository):
    
    user_id = 2
    
    operations =  [
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
        )
    ]
    
    data_repository.delete_operations(user_id=user_id, operations=operations)
    
    remaining_operation : Operation = data_repository.get_user_operations(user_id=2)[0]
    
    assert remaining_operation.is_equal(Operation(
            operation_id=6,
            user_id=2,
            operation_date=date(2025, 5, 22),
            category="Health",
            description="Pharmacy purchase",
            value=Decimal("-22.10"),
            currency="USD"
        ))
    
def test_delete_operations_using_ids(data_repository : DataRepository):
    
    user_id = 2
    
    operations = [4,5]
    
    data_repository.delete_operations(user_id=user_id, operations=operations)
    
    remaining_operation : Operation = data_repository.get_user_operations(user_id=2)[0]
    
    assert remaining_operation.is_equal(Operation(
            operation_id=6,
            user_id=2,
            operation_date=date(2025, 5, 22),
            category="Health",
            description="Pharmacy purchase",
            value=Decimal("-22.10"),
            currency="USD"
        ))
    
def test_delete_operations_empty_list(data_repository : DataRepository):
    
    user_id = 2
    
    operations = []
    
    data_repository.delete_operations(user_id=user_id, operations=operations)
    
    remaining_operations : List[Operation] = data_repository.get_user_operations(user_id=2)
    
    operations_list = [
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
    
    for a, b in zip(remaining_operations, operations_list):
        a.is_equal(b)
        

def test_update_operations_one_operation(data_repository : DataRepository):
    
    user_id = 2
    
    operations = [{
            "operation_id" : 4,
            "updated_fields" : {
                "category" : "Shopping"
            }
        }]
    
    data_repository.update_operations(user_id=user_id, operations=operations)
    
    updated_record = data_repository.get_user_operations(user_id=2)[0]
    
    assert updated_record.is_equal(Operation(
            operation_id=4,
            user_id=2,
            operation_date=date(2025, 5, 18),
            category="Shopping",
            description="Electricity bill",
            value=Decimal("-65.75"),
            currency="USD"
        ))

def test_update_operations_many_operations(data_repository : DataRepository):
    
    user_id = 2
    
    operations = [{
            "operation_id" : 4,
            "updated_fields" : {
                "category" : "Shopping"
            }
        },
        {
            "operation_id" : 5,
            "updated_fields" : {
                "category" : "Gaming"
            }
        },
        {
            "operation_id" : 6,
            "updated_fields" : {
                "category" : "Vacations"
            }
        }]
    
    data_repository.update_operations(user_id=user_id, operations=operations)

    correct_updated_operations = [
        Operation(
            operation_id=4,
            user_id=2,
            operation_date=date(2025, 5, 18),
            category="Shopping",
            description="Electricity bill",
            value=Decimal("-65.75"),
            currency="USD"
        ),
        Operation(
            operation_id=5,
            user_id=2,
            operation_date=date(2025, 5, 19),
            category="Gaming",
            description="Dinner at Luigi's",
            value=Decimal("-45.00"),
            currency="USD"
        ),
        Operation(
            operation_id=6,
            user_id=2,
            operation_date=date(2025, 5, 22),
            category="Vacations",
            description="Pharmacy purchase",
            value=Decimal("-22.10"),
            currency="USD"
        )
    ]
    
    for a,b in zip(data_repository.get_user_operations(user_id=2), correct_updated_operations):
        assert a.is_equal(b)


    
    
    
    
    
        