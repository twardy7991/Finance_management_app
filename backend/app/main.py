from fastapi import FastAPI
from app.endpoints.routes import Routing
from .containers import Container

def create_app() -> FastAPI:

    container = Container()   
    db = container.db()    
    
    app = FastAPI()
    apirouter = Routing()
    apirouter.configure_routes()
    app.include_router(apirouter.router)

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


app = create_app()