### MODELS FOR ROUTES ###

from datetime import date
from typing import List

from pydantic import BaseModel

class Operation(BaseModel):
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

class Credentials(BaseModel):
    username : str
    password : str

class CreateUserRequest(Credentials, User):
    pass

class Data(BaseModel):
    intercept : float
    coeff : List[float] 
    prediction : List[float]

class Session(BaseModel):
    session_id : str
        
