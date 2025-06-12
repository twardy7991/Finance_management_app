from pydantic import BaseModel
from datetime import date

class UserId(BaseModel):
    user_id : int
    
class OperationOut(BaseModel):
    operation_date : date
    category : str
    description : str
    value : float
    currency : str
    
    class Config:
        orm_mode = True