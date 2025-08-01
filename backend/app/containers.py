from fastapi.security import OAuth2PasswordBearer
from dependency_injector import containers, providers

from .db import Database
from app.database.repositories import DataRepository, UserRepository, CredentialRepository
from app.services.authentication_services import AuthenticationService
from app.services.compute_service import ComputingService
from app.services.user_service import UserService
from app.services.data_service import DataService
from app.auth.auth import AuthenticationTools 
from app.services.utils.clients import ComputeClient

### CONTAINER CLASS THAT CONSTRUCTS ALL DEPENDENCIES ### 

class Container(containers.DeclarativeContainer):
    
    wiring_config = containers.WiringConfiguration(modules=[".endpoints.routes"])
    
    config = providers.Configuration()
    config.from_yaml("config/config.yml")
    
    db = providers.Singleton(Database, db_url=config.db.url) 
    
    # utils/clients
    auth_tools = providers.Factory(
        AuthenticationTools,
    )
    
    oauth2_bearer = providers.Factory(
        oauth2_bearer=OAuth2PasswordBearer(tokenUrl='auth/token')
    )
    
    compute_client = providers.Factory(
        ComputeClient,
        base_url = config.compute.url
    )
    
    # repositories
    user_repository = providers.Factory(  
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
    
    # services
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
    
    compute_service = providers.Factory(
        ComputingService,
        compute_client = compute_client,
        data_repository = data_repository
    )
    

    

    
