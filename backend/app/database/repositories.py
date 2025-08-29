from datetime import date, datetime
from typing import List, Tuple, Literal, Dict
import logging
import abc
from decimal import Decimal

from sqlalchemy.orm import Session
from sqlalchemy import select, insert, delete, update, Delete, Select, Insert
from pandas import DataFrame

from app.database.models import Operation, User, Credential, UserSession
from app.database.exceptions import UserNotSavedError, DataNotFound 
from app.database.utils.utils import stmt_parser, data_frame_to_operation_list

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG) 
handler = logging.StreamHandler()  
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

## ABSTRACT CLASS FOR REPOSITORIES ##
 
class Repository(abc.ABC):
    
    def __init__(self, session : Session):
        
        self._session : Session = session

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
        
            stmt : Select = stmt_parser(user_id=user_id, 
                            date_from=date_from, 
                            date_to=date_to, order=order, 
                            operation_type=operation_type, 
                            group_by=group_by)
        
            result = list(self._session.scalars(stmt))
            
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
        
        self._session.bulk_save_objects(operations)
        
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
            
        self._session.execute(
            update(Operation), 
            update_params
            )

    def delete_operations(self, user_id, operations : List[Operation] | List[int]):
        
        if operations and isinstance(operations[0], Operation):  
            operations : List[int] = [o.operation_id for o in operations]
        
        stmt : Delete = delete(Operation).where(Operation.operation_id.in_(tuple(operations)), Operation.user_id == user_id)
        
        self._session.execute(stmt)

### CLASS RESPONSIBLE FOR QUERYING USER SPECIFIC DATA ###
     
class UserRepository(Repository):
        
        def get_user(self, user_id : int) -> User:

            stmt = select(User).where(User.user_id == user_id)
            
            result = list(self._session.scalars(stmt))
            
            logger.debug(f"Fetched user info for user_id={user_id} : {result}")
            
            return result[0]
            
            #return None

        def save_user(self ,
                name : str, 
                surname : str, 
                telephone : str, 
                address : str
                ) -> int:
            
            stmt : Insert = insert(User).values(name=name, surname=surname, telephone=telephone, address=address)

            result = self._session.execute(stmt)
            
            pk : int = result.inserted_primary_key[0]
            
            if pk is None:
                raise UserNotSavedError
            
            return pk
        
        def update_user(self, user_id, data):
                
            update_params = [{
                    "user_id" : user_id,
                    **data[0]["updated_fields"]
                    }]

            self._session.execute(
                update(User), 
                update_params
            )

            self._session.commit()
        
        def delete_user(self, user_id : int):
                
            if user_id and isinstance(user_id, User):  
                user_id : int = user_id.user_id
            
            stmt : Delete = delete(User).where(User.user_id == user_id)
            
            self._session.execute(stmt)
            
### CLASS RESPONSIBLE FOR QUERYING CREDENTIAL DATA ###  
                             
class CredentialRepository(Repository):
    
    def save_credentials(self, 
                         user_id : int, 
                         username : str, 
                         hashed_password : str
                         ) -> None:
        
        stmt = insert(Credential).values(user_id=user_id, username=username, password=hashed_password)
        
        self._session.execute(stmt)
        
        logger.debug(f"saved credentials for user {user_id}")
                
            
    def get_credentials(self, 
                        username : str
                        ) -> Tuple[int, str, str]:
        
        stmt = select(Credential).where(Credential.username==username)
        
        result : Credential = self._session.scalar(stmt)
        
        logger.debug(f"Fetched credentials for username={username} : {result}")
        logger.debug(f"class : {type(Credential)}")

        return result
    
    # def delete_credentials(self,
    #                        username : str):
        
    #     stmt = delete
    
class SessionRepository(Repository):
    
    def save_session(self, 
                    session_id : str, 
                    user_id : int,
                    created_at : datetime,
                    expires_at : datetime,
                    last_active : datetime,
                    roles : List[str],
                    metadata : Dict[str, str]
                    ) -> None:
        
        stmt : Insert = insert(UserSession).values(session_id=session_id, user_id=user_id, created_at=created_at, expires_at=expires_at, last_active=last_active, roles=roles, session_metadata=metadata)

        self._session.execute(stmt)
        
        return
    
    def get_session(self, session_id : int) -> UserSession:
        
        stmt : Select = select(UserSession).where(UserSession.session_id == session_id)
        
        result : UserSession = self._session.scalar(stmt)
        
        if result:
            logger.debug(f"Fetched Session for user_id={result.user_id} : {result}")
        
        return result
    
    def delete_session(self, user_id : int) -> None:
        
        logger.debug(user_id)
        
        stmt : Delete = delete(UserSession).where(UserSession.user_id == user_id)
        
        self._session.execute(stmt)
        
        logger.debug(f"Deleted session for user: {user_id}")