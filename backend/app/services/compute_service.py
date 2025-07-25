from app.services.utils.clients import ComputeClient
from app.database.repositories import DataRepository
from app.database.models import Operation
from app.services.utils.data_processing import date_to_int
from app.services.exceptions.exceptions import OperationsNotFoundError 

from datetime import date
from typing import List

class ComputingService:
    
    def __init__(self, compute_client : ComputeClient, data_repository : DataRepository):
        
        self.compute_client = compute_client
        self.data_repository = data_repository
        
    def calculate_trend(self,
                        user_id : int,
                        date_from : date = None,
                        date_to : date = None
                        ) -> List[List[int]]:
        
        operations : List[Operation] = self.data_repository.get_user_operations(user_id=user_id,
                                                date_from=date_from,
                                                date_to=date_to,
                                                type="spendings")
        
        if len(operations) < 1: 
            raise OperationsNotFoundError("Operations not found for selected period")
        
        preprocessed_data = date_to_int(operations)
        
        data = self.compute_client.send_request(preprocessed_data)
        
        return data