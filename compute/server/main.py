from fastapi import FastAPI
from routes import router
from containers import Container

def create_app():
    container = Container()
    app = FastAPI()
    app.container = container
    app.include_router(router)
    
    return app

app = create_app()