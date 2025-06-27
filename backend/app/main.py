from fastapi import FastAPI
from app.endpoints.routes import Routing
from .containers import Container
import uvicorn
from contextlib import asynccontextmanager
from app.containers import Container
from sqlalchemy import text

def app() -> FastAPI:

    container = Container()   
    container.wire(modules=[".endpoints.routes"]) 
    
    @asynccontextmanager
    async def lifespan(app: FastAPI):
        print("Application startup...")
        try:
            db_service = container.db()
            db_service.check_connection()
        except ConnectionError as e:
            print(f"Critical Error: Could not connect to the database.")
            raise RuntimeError("Database not available. The application will not start.") from e

        yield

        print("Application shutdown.")
    
    # Create app and routing
    app = FastAPI(lifespan=lifespan)
    
    router = Routing()
    
    # Setup injected routes after wiring
    router.setup_injected_routes()
    
    app.include_router(router.router)
    return app


    
    
    
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