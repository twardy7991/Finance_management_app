from dependency_injector import containers, providers

from models import Regression
import services

### CLASS THAT CONSTRUCTS ALL DEPENDENCIES FOR COMPUTING SERVER ###
class Container(containers.DeclarativeContainer):
    
    config = providers.Configuration()
    
    wiring_config = containers.WiringConfiguration(modules=["routes"])
    
    lr = providers.Factory(
        Regression
    )
    
    model_service = providers.Factory(
        services.ModelService,
        lr=lr
    )