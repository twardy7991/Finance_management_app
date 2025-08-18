from datetime import date
from typing import List

from app.services.utils.clients import ComputeClient
from app.database.models import Operation
from app.services.utils.data_processing import date_to_int
from app.services.exceptions.exceptions import OperationsNotFoundError 
from .utils.unit import UnitOfWorkOperation

### CLASS RESPONSIBLE FOR COMPUTING SERVICES ###

class ComputingService:
    
    def __init__(self, compute_client : ComputeClient, operation_uow : UnitOfWorkOperation):
        
        self.operation_uow = operation_uow
        self.compute_client = compute_client

    def calculate_trend(self,
                        user_id : int,
                        date_from : date = None,
                        date_to : date = None
                        ) -> List[List[int]]:
        
        with self.operation_uow as uow:
            
            operations : List[Operation] = uow.repository.get_user_operations(user_id=user_id,
                                                    date_from=date_from,
                                                    date_to=date_to,
                                                    operation_type="spendings")

        if len(operations) < 1: 
            raise OperationsNotFoundError("Operations not found for selected period")
        
        return self.compute_client.send_request(date_to_int(operations)) 