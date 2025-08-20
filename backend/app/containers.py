from fastapi.security import OAuth2PasswordBearer
from dependency_injector import containers, providers
from sqlalchemy.orm import DeclarativeBase

from app.db import Database, Base, Base_auth
from app.services.utils.unit import UnitOfWorkRegistration, UnitOfWorkCredential, UnitOfWorkOperation, UnitOfWorkUser, UnitOfWorkSession
from app.auth.auth import AuthenticationTools 
from app.services.utils.clients import ComputeClient
from app.services import SessionService, ComputingService, DataService, UserService, AuthenticationService

### CONTAINER CLASS THAT CONSTRUCTS ALL DEPENDENCIES ### 

class Container(containers.DeclarativeContainer):
    
    wiring_config = containers.WiringConfiguration(modules=[".endpoints.routes"])
    
    config = providers.Configuration()
    config.from_yaml("config/config.yml")
    
    db = providers.Singleton(Database, db_url=config.db.url) 
    db_auth = providers.Singleton(Database, db_url=config.db_auth.url)   
    
    # utils/clients
    auth_tools = providers.Factory(
        AuthenticationTools,
    )
    
    # oauth2_bearer = providers.Factory(
    #     oauth2_bearer=OAuth2PasswordBearer(tokenUrl='auth/token')
    # )
    
    compute_client = providers.Factory(
        ComputeClient,
        base_url = config.compute.url
    )
        
    # uow
    uow_registration = providers.Factory(
        UnitOfWorkRegistration,
        session_factory=db.provided.session_factory
    )
    
    user_uow = providers.Factory(
        UnitOfWorkUser,
        session_factory=db.provided.session_factory,
    )
    
    credential_uow = providers.Factory(
        UnitOfWorkCredential,
        session_factory=db.provided.session_factory,
    )
    
    operation_uow = providers.Factory(
        UnitOfWorkOperation,
        session_factory=db.provided.session_factory,
    )
    
    session_uow = providers.Factory(
        UnitOfWorkSession,
        session_factory=db_auth.provided.session_factory
    )
    
    # services
    auth_service = providers.Factory(
        AuthenticationService,
        auth_tools=auth_tools,
        credential_uow=credential_uow
    )
    
    user_service = providers.Factory(
        UserService,
        uow_registration=uow_registration,
        user_uow=user_uow,
        auth_tools=auth_tools
    ) 
    
    data_service = providers.Factory(
        DataService,
        operation_uow=operation_uow
    )
    
    compute_service = providers.Factory(
        ComputingService,
        compute_client = compute_client,
        operation_uow=operation_uow
    )
    
    session_service = providers.Factory(
        SessionService,
        session_uow=session_uow,
        auth_tools=auth_tools
    )
    

    

    
