from pydantic import BaseModel
from datetime import date
from fastapi import UploadFile

class OperationConditions(BaseModel):
    user_id : int 
    date_from: date | None = None
    date_to: date | None = None

class OperationOut(BaseModel):
    operation_date : date
    category : str
    description : str
    value : float
    currency : str
    
    class Config:
        orm_mode = True
