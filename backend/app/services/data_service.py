from datetime import date
from typing import List, BinaryIO

import pandas as pd

from .utils.unit import UnitOfWorkOperation
from app.database.models import Operation
from app.services.utils.data_processing import process_file, get_unsaved_operations

### CLASS RESPONSIBLE FOR USER DATA SERVICES ###    

class DataService:
    
    def __init__(self, operation_uow : UnitOfWorkOperation):
        self.operation_uow = operation_uow 
    
    def get_user_operations(self, 
                            user_id: int, 
                            date_from : date | None = None,
                            date_to : date | None = None,
                            order : str = "asc",
                            operation_type : str | None = None,
                            group_by : str | None = None
                            ) -> List[Operation]:

        with self.operation_uow as uow:
            return uow.repository.get_user_operations(user_id=user_id, 
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
        
        date_to : date = processed_data_file["#Data operacji"].iloc[0].date()
        date_from : date = processed_data_file["#Data operacji"].iloc[-1].date()
        
        with self.operation_uow as uow:
            saved_operations : List[Operation] = uow.repository.get_user_operations(user_id, date_from, date_to)
        
        operations_to_add : pd.DataFrame = get_unsaved_operations(saved_operations, processed_data_file)
        
        with self.operation_uow as uow:
            uow.repository.add_operations(operations_to_add, user_id)