from app.database.repositories import DataRepository
from sqlalchemy.orm import Session
from app.services.data_service import DataService

from operator import attrgetter
from pathlib import Path

filepath = Path(__file__).parent

## probably a wrong contructed tests, for further review ##

def test_save_user_operations(session : Session, operations_to_save):
        
    data_repository = DataRepository(session)
    data_service = DataService(data_repository)
    
    with open(f"{filepath}/data/lista_operacji_small.csv", "r") as f: 
        print("plik", type(f))
        data_service.save_user_operations(user_id = 2, datafile=f)
    
    saved_operations = data_repository.get_user_operations(user_id = 2)
    
    assert len(saved_operations) == len(operations_to_save)
    
    saved_operations = sorted(saved_operations, key=attrgetter('description'))
    
    operations_to_save = sorted(operations_to_save, key=attrgetter('description'))
    
    #assert operations == saved_operations
    
    # ugly workaround, gonna have to change it for something prettier
    for saved, expected in zip(saved_operations, operations_to_save):
        assert saved.is_equal(expected)

def test_get_user_operations(session, operations_in_database):
    
    data_repository = DataRepository(session)
    data_service = DataService(data_repository)
    
    for saved, expected in zip(data_service.get_user_operations(user_id=2), operations_in_database):
        assert saved.is_equal(expected)