from app.database.repositories import DataRepository
from datetime import date
from typing import List, BinaryIO
from app.database.models import Operation
import pandas as pd
from app.services.utils.data_processing import process_file, get_unsaved_operations

class DataService:
    
    def __init__(self, data_repository : DataRepository):
        
        self.data_repository : DataRepository = data_repository    
    
    def get_user_operations(self, 
                            user_id: int, 
                            data_from : date | None = None,
                            data_to : date | None = None,
                            ) -> List[Operation]:
    
        return self.data_repository.get_user_operations(user_id, 
                                                   data_from, 
                                                   data_to)
    
    def save_user_operations(self,
                             user_id : int,
                             datafile: BinaryIO
                             ) -> pd.DataFrame:
        
        processed_data_file : pd.DataFrame = process_file(datafile)
        print(f'asdfwGFAWG \n {processed_data_file}')
            # 1. Aby wyświetlić wszystkie wiersze (bez ograniczeń na liczbę wierszy)
        pd.set_option('display.max_rows', None)

        # 2. Aby wyświetlić wszystkie kolumny (bez ograniczeń na liczbę kolumn)
        pd.set_option('display.max_columns', None)
        
        
        date_to = processed_data_file["#Data operacji"].iloc[0].date()
        date_from = processed_data_file["#Data operacji"].iloc[-1].date()
        print(f"ASDAWFQWFQWFQ \n {date_from}, {date_to}")
        saved_operations = self.data_repository.get_user_operations(user_id, date_from, date_to)
        
        operations_to_add = get_unsaved_operations(saved_operations, processed_data_file)
        
        self.data_repository.add_operations(operations_to_add, user_id)