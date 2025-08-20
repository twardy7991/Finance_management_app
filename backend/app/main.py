from contextlib import asynccontextmanager

from fastapi import FastAPI
from dependency_injector.wiring import Provide

from app.endpoints.routes import router, protected_router
from app.containers import Container

from app.db import Base_auth, Base
### PROJECT MAIN CLASS ###

def create_app() -> FastAPI:
    
    container = Container()   
      
    print("Loaded config:", container.config())
    
    @asynccontextmanager
    async def lifespan(app: FastAPI):
        print("Application startup...")
        
        try:
            db_service = container.db()
            db_auth_service = container.db_auth()
            db_service.check_connection()    

            Base.metadata.create_all(bind=db_service.get_engine())
            Base_auth.metadata.create_all(bind=db_auth_service.get_engine())
            
        except ConnectionError as e:
            raise RuntimeError("Database not available. The application will not start.") from e
        yield

        print("Application shutdown.")
        
    app = FastAPI(lifespan=lifespan)
    app.container = container
    
    app.include_router(router)
    app.include_router(protected_router)
    
    return app

app = create_app()