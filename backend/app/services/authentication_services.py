from typing import Tuple

from app.auth.auth import AuthenticationTools
from app.services.user_service import UserService
from app.services.exceptions import UserNotFoundError, PasswordIncorrectError, TokenNotValidError

### CLASS RESPONSIBLE FOR PROVIDING AUTHENTICATION SERVICES ###

class AuthenticationService:
    
    def __init__(self, user_service : UserService, auth_tools : AuthenticationTools):    
        
        self.user_service : UserService = user_service
        self.auth_tools = auth_tools
        
    def register_user(self, username : str, 
                      password : str,
                      name : str,
                      surname : str,
                      telephone : str,
                      address : str
                      ) -> None:
        
        return self.user_service.register_user(username=username, 
                                                password=self.auth_tools.hash(password),
                                                name=name,
                                                surname=surname,
                                                telephone=telephone,
                                                address=address)
        
    def login_user(self, 
                   user_id : int, 
                   username : str, 
                   password : str
                   ) -> str:
        
        db_username, db_password = self.user_service.get_credential(username=username)
        
        if db_username is None:
            raise UserNotFoundError
        
        if self.auth_tools(password=password, hashed_password=db_password):
            return self.auth_tools.create_access_token(user_id=user_id, username=username)
        else:
            raise PasswordIncorrectError
    
    def check_user_token(self, token : str) -> Tuple[str, int]:
        
        username, user_id = self.auth_tools.check_token(token)
        if username is None or user_id is None:
            raise TokenNotValidError
        
        return username, user_id
        