from app.database.repositories import UserRepository, CredentialRepository
from app.database.models import User
from app.services.authentication_service import AuthenticationService
from .utils.unit import UnitOfWorkRegistration
from app.auth.auth import AuthenticationTools

### CLASS RESPONSIBLE THE USER SERVICES ###

class UserService:
    
    def __init__(self, uow_registration : UnitOfWorkRegistration, user_repository : UserRepository, auth_tools : AuthenticationTools):
        
        self.user_repository = user_repository
        self.uow_registration = uow_registration
        self.auth_tools = auth_tools
    
    def register_user(self, username : str, 
                    password : str,
                    name : str,
                    surname : str,
                    telephone : str,
                    address : str
                    ) -> int | None:
        
        with self.uow_registration as uow:
            
            user_id = uow.user_repository.save_user(name=name, 
                                                 surname=surname, 
                                                 telephone=telephone, 
                                                 address=address)
        
            uow.credential_repository.save_credentials(user_id=user_id,
                                username=username, 
                                hashed_password=self.auth_tools.hash(password))

            uow.commit()
            
        return user_id 
    
    def get_user(self, user_id : int) -> User:
        return self.user_repository.get_user(user_id=user_id)