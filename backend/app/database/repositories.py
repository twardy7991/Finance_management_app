from sqlalchemy import select, insert
from app.database.models.models import Operation
from sqlalchemy.orm import Session, sessionmaker
from typing import List
from datetime import date
import logging
from pandas import DataFrame

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)  # Or INFO
handler = logging.StreamHandler()  # Logs to stderr
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

class NotFound(Exception):
    
    entity: str
    
    def __init__(self, entity):
        super().__init__(f"{self.entity} not found")

class DataNotFound(NotFound):
    
    entity: str = "Data"

class DataRepository:

    def __init__(self, session_factory : sessionmaker[Session]) -> List[Operation]:
        
        self.session_factory : Session = session_factory
        
    def get_user_operations(self, 
                            user_id: int | None, 
                            date_from : date | None = None,
                            date_to : date | None = None):
        
        conditions = []
        
        if user_id is not None:
            conditions.append(Operation.user_id == user_id)
            
        if date_from is not None:
            conditions.append(Operation.operation_date >= date_from)
        
        if date_to is not None:
            conditions.append(Operation.operation_date <= date_to)
        
        stmt = select(Operation).where(*conditions)

        with self.session_factory() as session:
            session : Session
            
            result = list(session.scalars(stmt))
            
            values : List[Operation] = list(result)

            logger.debug(f"Fetched operations for user_id={user_id}: {values}")

            if values is None:
                raise DataNotFound
        
            return values
    
    def get_operation_by_id(self, user_id : int, operation_id : int) -> Operation:
        
        stmt = select(Operation).where(Operation.user_id == user_id, Operation.operation_id == operation_id)
        
        with self.session_factory() as session:
            
            session : Session
            
            value : Operation = session.scalars(stmt)
            
            if not value:
                raise DataNotFound

            return value
        
    def add_operations(self, data_file : DataFrame, user_id : int):
        
        # stmt = insert(Operation).values(data_file)
        
        # with self.session_factory() as session:
            
        #     data_file.to_sql("financial_operations", con=session, method='multi')
        
        print("hi")
        
        operations = [Operation(
                user_id=user_id,
                operation_date=row["#Data operacji"],
                category=row["#Kategoria"],
                description=row["#Opis operacji"],
                value=row["Kwota"],
                currency=row["Waluta"]) 
                for _, row in data_file.iterrows()]
        
        with self.session_factory() as session:
            
            session : Session
            
            session.bulk_save_objects(operations)
            
            session.commit()
        
        
class UserRepository:
    
    def __init__(self):
        raise NotImplementedError
        
