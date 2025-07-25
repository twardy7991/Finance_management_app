from app.database.models import Operation, User, Credential
from app.database.exceptions import UserNotProvidedError, UserNotSavedError, DataNotFound 
from app.database.utils.utils import stmt_parser

from sqlalchemy.orm import Session, sessionmaker
from typing import List, Tuple
from datetime import date
from sqlalchemy import select, insert
import logging
from pandas import DataFrame


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG) 
handler = logging.StreamHandler()  
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

class DataRepository:

    def __init__(self, session_factory : sessionmaker[Session]):
        
        self.session_factory : Session = session_factory
        
    def get_user_operations(self, 
                            user_id: int, 
                            date_from : date | None = None,
                            date_to : date | None = None,
                            order : str | None = "asc",
                            type : str | None = None,
                            group_by : str | None = None
                            ) -> List[Operation]:
        
        stmt = stmt_parser(user_id, date_from, date_to, order, type, group_by)
        
        with self.session_factory() as session:
            
            session : Session
            
            result = list(session.scalars(stmt))
            
            values : List[Operation] = list(result)

            logger.debug(f"Fetched operations for user_id={user_id} : {values}")

            if values is None:
                raise DataNotFound
        
            return values
        
    def add_operations(self, 
                       data_file : DataFrame, 
                       user_id : int
                       ) -> None:
        
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
    
        def __init__(self, session_factory : sessionmaker[Session]) -> int:
        
            self.session_factory : Session = session_factory
            
        def save_user(self ,
                      name : str, 
                      surname : str, 
                      telephone : str, 
                      address : str
                      ) -> int:
            
            stmt = insert(User).values(name=name, surname=surname, telephone=telephone, address=address)
            
            with self.session_factory() as session:
                
                session : Session
                
                result = session.execute(stmt)

                print(result.inserted_primary_key)
                
                pk = result.inserted_primary_key
                
                if pk is None:
                    raise UserNotSavedError
                
                session.commit()
            
            return pk
                                    
class CredentialRepository:
    
    def __init__(self, session_factory : sessionmaker[Session]):
    
        self.session_factory : Session = session_factory
        
    def save_credentials(self, 
                         user_id : int, 
                         username : str, 
                         hashed_password : str
                         ) -> None:
        
        stmt = insert(Credential).values(user_id = user_id, username=username, password=hashed_password)
        
        with self.session_factory() as session:
            
            session : Session
            
            result = session.execute(stmt)

            print(result.inserted_primary_key)
    
            session.commit()
            
            
    def get_credentials(self, 
                        username : str
                        ) -> Tuple[int, str, str]:
        
        stmt = select(Credential).where(username=username)
        
        with self.session_factory() as session:
            
            session : Session
            
            result : Credential = session.scalar(stmt)
            
            session.commit()
            
            return result.user_id, result.username, result.password 