### MAIN CLASS FOR COMPUTING SERVER ###

from fastapi import FastAPI
from containers import Container

from routes import router

def create_app():
    container = Container()
    app = FastAPI()
    app.container = container
    app.include_router(router)
    
    return app

app = create_app()