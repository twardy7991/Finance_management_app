from app.database.models import User
from .utils.unit import UnitOfWorkRegistration, UnitOfWorkUser
from app.auth.auth import AuthenticationTools
from sqlalchemy.exc import IntegrityError
from .exceptions import DuplicateUsernameError
### CLASS RESPONSIBLE THE USER SERVICES ###

class UserService:
    
    def __init__(self, user_uow : UnitOfWorkUser, uow_registration : UnitOfWorkRegistration, auth_tools : AuthenticationTools):
        
        self.uow_registration = uow_registration
        self.auth_tools = auth_tools
        self.user_uow = user_uow
    
    def register_user(self, username : str, 
                    password : str,
                    name : str,
                    surname : str,
                    telephone : str,
                    address : str
                    ) -> int | None:
        
        with self.uow_registration as uow:
            
            user_id : int = uow.user_repository.save_user(name=name, 
                                                    surname=surname, 
                                                    telephone=telephone, 
                                                    address=address)    
                
            try: 
                uow.credential_repository.save_credentials(user_id=user_id,
                                    username=username, 
                                    hashed_password=self.auth_tools.hash(password))
            except IntegrityError as e:
                raise DuplicateUsernameError
            
            uow.commit()
                
        return user_id 
    
    def get_user(self, user_id : int) -> User:
        with self.user_uow as uow:
            return uow.repository.get_user(user_id=user_id)