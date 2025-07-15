from app.database.repositories import DataRepository
from app.database.models.models import Operation
from app.services.data_processing import process_file, get_unsaved_operations

from typing import List, BinaryIO
from datetime import date
import pandas as pd

class DataService:
    
    def __init__(self, data_repository : DataRepository):
        
        self.data_repository : DataRepository = data_repository    
    
    def get_user_operations(self, 
                            user_id: int | None, 
                            data_from : date | None = None,
                            data_to : date | None = None,
                            ) -> List[Operation]:
    
        return self.data_repository.get_user_operations(user_id, 
                                                   data_from, 
                                                   data_to)
    
    def save_user_operations(self,
                             user_id : int,
                             datafile: BinaryIO) -> pd.DataFrame:
        
        processed_data_file : pd.DataFrame = process_file(datafile)
        
        date_from = processed_data_file["#Data operacji"].iloc[-1]
        date_to = processed_data_file["#Data operacji"].iloc[0]

        saved_operations = self.data_repository.get_user_operations(user_id, date_from, date_to)
        
        operations_to_add = get_unsaved_operations(saved_operations, processed_data_file)
        
        self.data_repository.add_operations(operations_to_add, user_id)
    
class UserService:
    
    def __init__(self):
        pass