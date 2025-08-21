from typing import Tuple

from app.auth.auth import AuthenticationTools
from app.services.exceptions import PasswordIncorrectError, UsernameIncorrectError
from app.database.models import Credential
from .utils.unit import UnitOfWorkCredential
### CLASS RESPONSIBLE FOR PROVIDING AUTHENTICATION SERVICES ###

class AuthenticationService:
    
    def __init__(self, credential_uow : UnitOfWorkCredential, auth_tools : AuthenticationTools):    
        
        self.credential_uow = credential_uow
        self.auth_tools = auth_tools
    
    def login_user(self, 
                   username : str, 
                   password : str
                   ) -> str:
        
        credential : Credential = self.get_credential(username=username)

        if credential is None or credential.username != username:
            raise UsernameIncorrectError
        elif not self.auth_tools.compare_hash(password=password, hashed_password=credential.password):
            raise PasswordIncorrectError
        else:
            return credential.user_id
            
    
    def check_user_token(self, token : str) -> Tuple[str, int]:
        pass
        # username, user_id = self.auth_tools.check_token(token)
        # if username is None or user_id is None:
        #     raise TokenNotValidError
        
        # return username, user_id
    
    def get_credential(self, username : str) -> Credential:
        with self.credential_uow as uow:
            return uow.repository.get_credentials(username=username)
        