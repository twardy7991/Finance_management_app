from datetime import date
from typing import List, BinaryIO

import pandas as pd

from app.database.repositories import DataRepository
from app.database.models import Operation
from app.services.utils.data_processing import process_file, get_unsaved_operations

### CLASS RESPONSIBLE FOR USER DATA SERVICES ###    

class DataService:
    
    def __init__(self, data_repository : DataRepository):
        
        self.data_repository : DataRepository = data_repository    
    
    def get_user_operations(self, 
                            user_id: int, 
                            date_from : date,
                            date_to : date,
                            order : str,
                            operation_type : str,
                            group_by : str
                            ) -> List[Operation]:
    
        return self.data_repository.get_user_operations(user_id=user_id, 
                                                   date_from=date_from, 
                                                   date_to=date_to,
                                                   order=order,
                                                   operation_type=operation_type,
                                                   group_by=group_by)
    
    def save_user_operations(self,
                             user_id : int,
                             datafile: BinaryIO
                             ):
        
        processed_data_file : pd.DataFrame = process_file(datafile)
        
        date_to = processed_data_file["#Data operacji"].iloc[0].date()
        date_from = processed_data_file["#Data operacji"].iloc[-1].date()
        saved_operations = self.data_repository.get_user_operations(user_id, date_from, date_to)
        
        operations_to_add = get_unsaved_operations(saved_operations, processed_data_file)
        
        self.data_repository.add_operations(operations_to_add, user_id)