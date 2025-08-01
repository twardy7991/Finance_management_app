from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.endpoints.routes import router
from app.containers import Container

### PROJECT MAIN CLASS ###

def create_app() -> FastAPI:
    
    container = Container()   
      
    print("Loaded config:", container.config())
    
    @asynccontextmanager
    async def lifespan(app: FastAPI):
        print("Application startup...")
        
        try:
            db_service = container.db()
            db_service.check_connection()    
            
        except ConnectionError as e:
            raise RuntimeError("Database not available. The application will not start.") from e
        yield

        print("Application shutdown.")
        
    app = FastAPI(lifespan=lifespan)
    app.container = container
    
    app.include_router(router)
    
    return app

app = create_app()