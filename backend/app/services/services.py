from app.database.repositories import DataRepository
from typing import List
from app.database.models.models import Operation

class DataService:
    
    def __init__(self, data_repository : DataRepository):
        
        self.repository : DataRepository = data_repository
        
    def get_user_operations(self, user_id : int) -> List[Operation]:
        return self.repository.get_user_operations(user_id)
    
class UserService:
    
    def __init__(self):
        pass