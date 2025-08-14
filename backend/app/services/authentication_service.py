from typing import Tuple

from app.auth.auth import AuthenticationTools
from app.services.exceptions import UserNotFoundError, PasswordIncorrectError, UsernameIncorrectError
from app.database.repositories import CredentialRepository
from app.database.models import Credential
### CLASS RESPONSIBLE FOR PROVIDING AUTHENTICATION SERVICES ###

class AuthenticationService:
    
    def __init__(self, credential_repository : CredentialRepository, auth_tools : AuthenticationTools):    
        
        self.credential_repository = credential_repository
        self.auth_tools = auth_tools
        
    def save_credentials(self, user_id, username, password):
        
        self.credential_repository.save_credentials(user_id=user_id,
                                        username=username, 
                                        hashed_password=self.auth_tools.hash(password))
        
    def login_user(self, 
                   username : str, 
                   password : str
                   ) -> str:
        
        credential = self.get_credential(username=username)

        if credential is None or credential.username != username:
            raise UsernameIncorrectError
        elif not self.auth_tools.compare_hash(password=password, hashed_password=credential.password):
            raise PasswordIncorrectError
        else:
            return
            
    
    def check_user_token(self, token : str) -> Tuple[str, int]:
        
        pass
        # username, user_id = self.auth_tools.check_token(token)
        # if username is None or user_id is None:
        #     raise TokenNotValidError
        
        # return username, user_id
    
    def get_credential(self, username : str) -> Credential:
        return self.credential_repository.get_credentials(username=username)
        