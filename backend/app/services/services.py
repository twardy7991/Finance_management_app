from app.database.repositories import DataRepository, UserRepository, CredentialRepository
from app.database.models.models import Operation
from app.services.data_processing import process_file, get_unsaved_operations
from app.auth.auth import AuthenticationTools

from typing import List, BinaryIO
from datetime import date
import pandas as pd

from app.services.exceptions import UserNotFoundError, PasswordIncorrectError, TokenNotValidError

class DataService:
    
    def __init__(self, data_repository : DataRepository):
        
        self.data_repository : DataRepository = data_repository    
    
    def get_user_operations(self, 
                            user_id: int, 
                            data_from : date | None = None,
                            data_to : date | None = None,
                            ) -> List[Operation]:
    
        return self.data_repository.get_user_operations(user_id, 
                                                   data_from, 
                                                   data_to)
    
    def save_user_operations(self,
                             user_id : int,
                             datafile: BinaryIO) -> pd.DataFrame:
        
        processed_data_file : pd.DataFrame = process_file(datafile)
        
        date_from = processed_data_file["#Data operacji"].iloc[-1]
        date_to = processed_data_file["#Data operacji"].iloc[0]

        saved_operations = self.data_repository.get_user_operations(user_id, date_from, date_to)
        
        operations_to_add = get_unsaved_operations(saved_operations, processed_data_file)
        
        self.data_repository.add_operations(operations_to_add, user_id)
    
class UserService:
    
    def __init__(self, user_repository : UserRepository, credential_repository : CredentialRepository):
        
        self.user_repository : UserRepository = user_repository
        self.credential_repository : CredentialRepository = credential_repository
        
    def register_user(self, 
                      username : str, 
                      hashed_password : str,
                      name : str,
                      surname : str,
                      telephone : str,
                      address : str):
        
        # we need user_id to save credentials to right user
        user_id = self.user_repository.save_user(name=name, 
                                                 surname=surname, 
                                                 telephone=telephone, 
                                                 address=address)
        
        self.credential_repository.save_credentials(user_id=user_id,
                                              username=username, 
                                              hashed_password=hashed_password)
    
    def get_credential(self, username : str):
        return self.credential_repository.get_credentials(username=username)
    
class AuthenticationService:
    
    def __init__(self, user_service : UserService, auth_tools : AuthenticationTools):    
        self.user_service : UserService = user_service
        self.auth_tools = auth_tools
        
    def register_user(self, username : str, 
                      password : str,
                      name : str,
                      surname : str,
                      telephone : str,
                      address : str):
        
        return self.user_service.register_user(username=username, 
                                                password=self.auth_tools.hash(password),
                                                name=name,
                                                surname=surname,
                                                telephone=telephone,
                                                address=address)
        
    def login_user(self, user_id : int, username : str, password : str):
        
        db_username, db_password = self.user_service.get_credential(username=username)
        
        if db_username is None:
            raise UserNotFoundError
        
        if self.auth_tools(password=password, hashed_password=db_password):
            return self.auth_tools.create_access_token(user_id=user_id, username=username)
        else:
            raise PasswordIncorrectError
    
    def check_user_token(self, token):
        
        username, user_id = self.auth_tools.check_token(token)
        if username is None or user_id is None:
            raise TokenNotValidError
        
        return username, user_id
        
        
            

    
