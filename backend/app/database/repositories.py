from datetime import date
from typing import List, Tuple, Literal, Dict, Union
import logging
import abc
from decimal import Decimal

from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import select, insert, delete, update, Delete, Select, Insert, Update
from pandas import DataFrame

from app.database.models import Operation, User, Credential
from app.database.exceptions import UserNotProvidedError, UserNotSavedError, DataNotFound 
from app.database.utils.utils import stmt_parser, data_frame_to_operation_list

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG) 
handler = logging.StreamHandler()  
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

## ABSTRACT CLASS FOR REPOSITORIES ##
 
class Repository(abc.ABC):
    
    def __init__(self, session_factory : sessionmaker[Session], session=None):
        
        self._session : Session = session
        self._session_factory : Session = session_factory

    @property
    def session(self):
        return self._session or self._session_factory() 
    
### CLASS RESPONSIBLE FOR QUERYING USER OPERATIONS DATA ###

class DataRepository(Repository):
    
    def get_user_operations(self, 
                            user_id: int, 
                            date_from : date | None = None,
                            date_to : date | None = None,
                            order : Literal["asc","desc"] | None = "asc",
                            operation_type : Literal["spendings","earnings"] | None = None,
                            group_by : str | None = None
                            ) -> List[Operation]:
        
        with self.session as session:
        
            stmt : Select = stmt_parser(user_id=user_id, 
                            date_from=date_from, 
                            date_to=date_to, order=order, 
                            operation_type=operation_type, 
                            group_by=group_by)
        
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
        
        operations : List[Operation] = data_frame_to_operation_list(user_id=user_id, data_file=data_file)
            
        with self.session as session:
        
            session.bulk_save_objects(operations)
            
            session.commit()
        
    def update_operations(self, 
                          user_id : int, 
                          operations : List[Dict[str, int | Dict[str, str | int | date | Decimal]]]):
            
        update_params = [
            {
                "user_id" : user_id,
                "operation_id" : o["operation_id"],
                **o["updated_fields"]
            } 
            for o in operations]
        
        with self.session as session:
            
            session.execute(
                update(Operation), 
                update_params
                )

            session.commit()

    def delete_operations(self, user_id, operations : List[Operation] | List[int]):
        
        if operations and isinstance(operations[0], Operation):  
            operations : List[int] = [o.operation_id for o in operations]
        
        stmt : Delete = delete(Operation).where(Operation.operation_id.in_(tuple(operations)), Operation.user_id == user_id)
        
        with self.session as session:
            
            session.execute(stmt)
            
            session.commit()
            

### CLASS RESPONSIBLE FOR QUERYING USER SPECIFIC DATA ###
     
class UserRepository(Repository):
        
        def get_user(self, user_id : int) -> User:
            
            with self.session as session:
                
                stmt = select(User).where(User.user_id == user_id)
                
                result = list(session.scalars(stmt))
                
                logger.debug(f"Fetched user info for user_id={user_id} : {result}")
                
                if result:
                    return result[0]
                
                return None

        def save_user(self ,
                name : str, 
                surname : str, 
                telephone : str, 
                address : str
                ) -> int:
            
            stmt : Insert = insert(User).values(name=name, surname=surname, telephone=telephone, address=address)
                
            with self.session as session:
                
                result = session.execute(stmt)
                
                pk : int = result.inserted_primary_key[0]
                
                if pk is None:
                    raise UserNotSavedError
                
                #session.commit()
                
                return pk
        
        def update_user(self, user_id, data):
                
            update_params = [{
                    "user_id" : user_id,
                    **data[0]["updated_fields"]
                    }]
            with self.session as session:
                
                session.execute(
                    update(User), 
                    update_params
                )

                session.commit()
        
        def delete_user(self, user_id : int):
                
            if user_id and isinstance(user_id, User):  
                user_id : int = user_id.user_id
            
            stmt : Delete = delete(User).where(User.user_id == user_id)
            
            with self.session as session:
                
                session.execute(stmt)
                
                session.commit()
            
### CLASS RESPONSIBLE FOR QUERYING CREDENTIAL DATA ###  
                             
class CredentialRepository(Repository):
    
    def save_credentials(self, 
                         user_id : int, 
                         username : str, 
                         hashed_password : str
                         ) -> None:
        
        stmt = insert(Credential).values(user_id=user_id, username=username, password=hashed_password)
            
        with self.session as session:
            
            session.execute(stmt)

            #session.commit()
            
            logger.debug(f"saved credentials for user {user_id}")
                
            
    def get_credentials(self, 
                        username : str
                        ) -> Tuple[int, str, str]:
        
        stmt = select(Credential).where(Credential.username==username)
        
        with self.session as session:
            
            result : Credential = session.scalar(stmt)
            
            logger.debug(f"Fetched credentials for user_id={username} : {result}")

            return result