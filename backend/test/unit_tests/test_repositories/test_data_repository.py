import pytest
from app.database.repositories import DataRepository, UserRepository
from app.database.models import Operation, User
from datetime import date
from decimal import Decimal
from app.database.exceptions import ParameterError
from typing import List

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
    
    

def test_delete_operations_using_objects(session):
    
    data_repository = DataRepository(session_factory=session)
    
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
    
def test_delete_operations_using_ids(session):
    
    data_repository = DataRepository(session_factory=session)
    
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
    
def test_delete_operations_empty_list(session):
    
    data_repository = DataRepository(session_factory=session)
    
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
        

def test_update_operations_one_operation(session):
    
    data_repository = DataRepository(session_factory=session)
    
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

def test_update_operations_many_operations(session):
    
    data_repository = DataRepository(session_factory=session)
    
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

def test_get_user(session):
    
    user_repository = UserRepository(session_factory=session)
    
    user_id = 2
    
    user = user_repository.get_user(user_id=user_id)
    
    assert user.is_equal(User(
        user_id=2,
        name="Jane",
        surname="Smith",
        telephone="987654321",
        address="456 Elm St, Springfield"
    ))

def test_update_user(session):
    
    user_repository = UserRepository(session_factory=session)
    user_id = 2
    
    data = [{
            "updated_fields" : {
                "address" : "Racławicka 6/4, Kraków"
            }
        }]
    
    user_repository.update_user(user_id=user_id, data=data)
    
    updated_user = user_repository.get_user(user_id=user_id)
    
    assert updated_user.is_equal(User(
        user_id=2,
        name="Jane",
        surname="Smith",
        telephone="987654321",
        address="Racławicka 6/4, Kraków"
    ))

def test_delete_user(session):
    
    user_repository = UserRepository(session_factory=session)
    user_id = 2
    
    user = user_repository.get_user(user_id=user_id)
    
    assert user.is_equal(User(
        user_id=2,
        name="Jane",
        surname="Smith",
        telephone="987654321",
        address="456 Elm St, Springfield"
    ))
    
    user_repository.delete_user(user_id=user_id)
    
    assert user_repository.get_user(user_id=user_id) == None
    
    
    
    
    
        