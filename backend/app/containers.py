from dependency_injector import containers, providers
from .db import Database
from .database.repositories import DataRepository, UserRepository
from .services.services import UserService, DataService


class Container(containers.DeclarativeContainer):
    
    wiring_config = containers.WiringConfiguration(modules=[".endpoints"])

    config = providers.Configuration(yaml_files=["config.yml"])
    
    db = providers.Singleton(Database, db_url=config.db.url) ##singleton creates the instance once and saves it
    
    user_repository = providers.Factory(  ## Factory as the name suggests creates the new instance every time it is called 
        UserRepository,
        session_factory=db.provided.session,
        )
    
    user_service = providers.Factory(
        UserService,
        user_repository=user_repository,
    )
    
    data_repository = providers.Factory(
        DataRepository,
        session_factory=db.factory.session,
    ) 
    
    data_service = providers.Factory(
        DataService,
        data_repository=data_repository,
    )