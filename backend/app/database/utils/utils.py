### UTILS FUNCTIONS FOR REPOSITORIES ###

from datetime import date
from typing import List, Tuple

from sqlalchemy import select, insert, Select
import pandas as pd

from app.database.models import Operation
from app.database.exceptions import UserNotProvidedError, ParameterError

def stmt_parser(user_id: int,
                date_from : date | None = None,
                date_to : date | None = None,
                order : str | None = "asc",
                operation_type : str | None = None,
                group_by : str | None = None
                )-> Select[Tuple[Operation]]:
    
    where_conditions = []
    
    where_conditions.append(Operation.user_id == user_id)
    
    if date_from is not None:
        where_conditions.append(Operation.operation_date >= date_from)
    
    if date_to is not None:
        where_conditions.append(Operation.operation_date <= date_to)
    
    if operation_type is not None:    
        match operation_type:
            case "spendings" : where_conditions.append(Operation.value < 0)
            case "earnings" : where_conditions.append(Operation.value > 0)
            case _ : raise ParameterError("wrong operation_type value")
            
    stmt = select(Operation).where(*where_conditions)
    
    match order:
        case "desc" : stmt = stmt.order_by(Operation.operation_date.desc())
        case "asc" : stmt = stmt.order_by(Operation.operation_date.asc())
        case _ : raise ParameterError("wrong order value")
    
    if group_by is not None:
        match group_by:
            case "date" : stmt = stmt.group_by(Operation.operation_date)
            case "category" : stmt = stmt.group_by(Operation.category)
            case "currency" : stmt = stmt.group_by(Operation.currency)
            case _ : raise ParameterError("wrong group_by value")

    return stmt

def data_frame_to_operation_list(user_id : int, 
                                 data_file : pd.DataFrame
                                 ) -> List[Operation]:

    return [Operation(user_id=user_id,
                            operation_date=row["#Data operacji"],
                            category=row["#Kategoria"],
                            description=row["#Opis operacji"],
                            value=row["Kwota"],
                            currency=row["Waluta"]) 
                            for _, row in data_file.iterrows()]
