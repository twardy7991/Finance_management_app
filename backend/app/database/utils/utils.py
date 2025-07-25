from datetime import date
from app.database.models import Operation
from app.database.exceptions import UserNotProvidedError
from sqlalchemy import select, insert, Select
from typing import Tuple

def stmt_parser(user_id: int,
                date_from : date | None = None,
                date_to : date | None = None,
                order : str | None = "asc",
                type : str | None = None,
                group_by : str | None = None
                )-> Select[Tuple[Operation]]:
    
    where_conditions = []
        
    if user_id is None:
        raise UserNotProvidedError
    
    where_conditions.append(Operation.user_id == user_id)
    
    if date_from is not None:
        where_conditions.append(Operation.operation_date >= date_from)
    
    if date_to is not None:
        where_conditions.append(Operation.operation_date <= date_to)
    
    if type is not None:    
        match type:
            case "spendings" : where_conditions.append(Operation.value < 0)
            case "earnings" : where_conditions.append(Operation.value > 0)
            
    stmt = select(Operation).where(*where_conditions)
        
    if order is "desc":
        order_condition = Operation.operation_date.desc()
    else:
        order_condition = Operation.operation_date.asc()
    
    if group_by is not None:
        match group_by:
            case "date" : group_by_condition = Operation.operation_date
            case "category" : group_by_condition = Operation.category 
            case "currency" : group_by_condition = Operation.currency  
            
        stmt.group_by(group_by_condition)
    
    stmt = select(Operation).where(*where_conditions).order_by(order_condition)
    
    return stmt

        
    