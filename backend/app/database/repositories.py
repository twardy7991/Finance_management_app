from sqlalchemy import select 
from app.db import SQLconnection
from app.database.models.models import Operation
from sqlalchemy.orm import Session, sessionmaker
from models import Operation
from contextlib import AbstractContextManager
from typing import List

class DataRepository:

    def __init__(self, session_factory : sessionmaker[Session]) -> List[Operation]:
        
        self.session_factory : Session = session_factory
        
    def get_user_operations(self, userid : int):
        
        stmt = select(Operation).where(Operation.user_id == userid)

        with self.session_factory.begin() as session:
            session : Session
            
            result = session.scalars(stmt)
            
            values : List[Operation] = list(result)

        if not values:
            raise DataNotFound()
        
        return values
    
    def get_operation_by_id(self, user_id : int, operation_id : int) -> Operation:
        
        stmt = select(Operation).where(Operation.user_id == user_id, Operation.operation_id == operation_id)
        
        with self.session_factory.begin() as session:
            
            session : Session
            
            value : Operation = list(session.scalars(stmt))
            
            if not value:
                raise DataNotFound

            return value
        
        
class UserRepository:
    
    def __init__(self):
        pass
        
class NotFound(Exception):
    
    entity: str
    
    def __init__(self, entity):
        super().__init__(f"{self.entity} not found")

class DataNotFound(NotFound):
    
    entity: str = "Data"