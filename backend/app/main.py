from fastapi import FastAPI
from app.endpoints.routes import router
from .containers import Container
from contextlib import asynccontextmanager
from app.containers import Container

class ConfigError(Exception):
    
    def __init__(self, message : str):
        super().__init__(f"config is incomplete: {message}")
        
class DatabaseURLMissingError(ConfigError):
    
    def __init__(self):
        super().__init__("database url is missing")

def create_app() -> FastAPI:
    
    container = Container()   
      
    print("Loaded config:", container.config())
    
    @asynccontextmanager
    async def lifespan(app: FastAPI):
        print("Application startup...")
        
        try:
            db_service = container.db()
            db_service.check_connection()    
            
        ##throwed if database is unavailable
        except ConnectionError as e:
            raise RuntimeError("Database not available. The application will not start.") from e
        yield

        print("Application shutdown.")
    
    # Create app and routing
    app = FastAPI(lifespan=lifespan)
    app.container = container
    
    app.include_router(router)
    return app

app = create_app()


# import os
# import pandas as pd

# # Path to this script (main.py)
# SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# # Go one level up to reach "Kalkulator finansowy"
# PARENT_DIR = os.path.dirname(SCRIPT_DIR)

# # Full path to the CSV file
# csv_path = os.path.join(PARENT_DIR, "data", "lista_operacji.csv")

# # Load the file
# operations = pd.read_csv(csv_path, skiprows=25, delimiter=';')