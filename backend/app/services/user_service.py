from app.database.repositories import UserRepository, CredentialRepository

from typing import Tuple

class UserService:
    
    def __init__(self, user_repository : UserRepository, credential_repository : CredentialRepository):
        
        self.user_repository = user_repository
        self.credential_repository = credential_repository
        
    def register_user(self, 
                      username : str, 
                      hashed_password : str,
                      name : str,
                      surname : str,
                      telephone : str,
                      address : str
                      ) -> None:
        
        # we need user_id to save credentials to right user
        user_id = self.user_repository.save_user(name=name, 
                                                 surname=surname, 
                                                 telephone=telephone, 
                                                 address=address)
        
        self.credential_repository.save_credentials(user_id=user_id,
                                              username=username, 
                                              hashed_password=hashed_password)
    
    def get_credential(self, username : str) -> Tuple[int, str, str]:
        return self.credential_repository.get_credentials(username=username)
    