### MODELS FOR ROUTES ###

from datetime import date
from typing import List

from pydantic import BaseModel

class OperationConditions(BaseModel):
    user_id : int 
    date_from : date | None = None
    date_to: date | None = None

class OperationOut(BaseModel):
    operation_date : date
    category : str
    description : str
    value : float
    currency : str
    
    class Config:
        orm_mode = True

class User(BaseModel):
    name : str
    surname: str
    telephone : str
    address : str

class CreateUserRequest(BaseModel):
    username : str
    password : str
    name : str
    surname: str
    telephone : str
    address : str
    
class Credentials(BaseModel):
    username : str
    password : str
    
class Token(BaseModel):
    access_token: str
    token_type: str
    
class Data(BaseModel):
    intercept : float
    coeff : List[float] 
    prediction : List[float]
        
