from fastapi import APIRouter, Depends, Response, status
from projects.Finance_calc.backend.app.database.repositories import DataService
from app.endpoints.schemas import UserId
from dependency_injector.wiring import Provide, inject
from database.repositories import DataNotFound
from typing import Annotated
from services.services import DataService
from containers import Container


## we create funtion to point to the get_session from SQLconnection class so we can use it in Depends() 
## we create is outside the class as Depends() cannot use self.*** as it is in function parentheses

class Routing:

    def __init__(self):
        self.router = APIRouter()

    def configure_routes(self): 

        @self.router.get("/")
        def root():
            return {"message": "Hello from FastAPI"}

        @self.router.post("/user/data")
        @inject
        def get_user_finance_data(
            userid: UserId, 
            data_service: Annotated[DataService, Depends(Provide[Container.data_service])],
            ):
            try:
                return data_service.get_user_operations(userid.user_id)
            except DataNotFound:
                return Response(staus_code=status.HTTP_404_NOT_FOUND)

        @self.router.get("/status")
        def get_status():
            return {"status": "OK"}