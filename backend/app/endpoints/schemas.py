from pydantic import BaseModel
from datetime import date

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
        
class CreateUserRequest(BaseModel):
    username: str
    password: str
    
class Token(BaseModel):
    access_token: str
    token_type: str
        
