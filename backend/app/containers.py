from dependency_injector import containers, providers
from .db import Database
from .database.repositories import DataRepository, UserRepository, CredentialRepository
from .services.services import UserService, DataService, AuthenticationService
from app.auth import auth
from fastapi.security import OAuth2PasswordBearer

class Container(containers.DeclarativeContainer):
    
    wiring_config = containers.WiringConfiguration(modules=[".endpoints.routes"])
    
    config = providers.Configuration()
    config.from_yaml("config/config.yml")
    
    db = providers.Singleton(Database, db_url=config.db.url) ##singleton creates the instance once and saves it
    
    user_repository = providers.Factory(  ## Factory as the name suggests creates the new instance every time it is called 
        UserRepository,
        session_factory=db.provided.session,
        )
    
    data_repository = providers.Factory(
        DataRepository,
        session_factory=db.provided.session,
    )
    
    credential_repository = providers.Factory(
        CredentialRepository,
        session_facory=db.provided.session,
    )
    
    user_service = providers.Factory(
        UserService,
        user_repository=user_repository,
    ) 
    
    data_service = providers.Factory(
        DataService,
        data_repository=data_repository,
    )
    
    auth_service = providers.Factory(
        AuthenticationService,
        user_service=user_service,
    )
    
    auth_tools = providers.Factory(
        auth,
    )
    
    oauth2_bearer = providers.Factory(
        oauth2_bearer=OAuth2PasswordBearer(tokenUrl='auth/token')
    )
    
    
