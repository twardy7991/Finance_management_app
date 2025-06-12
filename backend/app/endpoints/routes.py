from fastapi import APIRouter, Depends, Response, status, Body
from app.endpoints.schemas import UserId
from dependency_injector.wiring import Provide, inject
from app.database.repositories import DataNotFound
from typing import Annotated, List, Union
from app.services.services import DataService
from app.containers import Container
from app.endpoints.schemas import OperationOut

## we create funtion to point to the get_session from SQLconnection class so we can use it in Depends() 
## we create is outside the class as Depends() cannot use self.*** as it is in function parentheses

class Routing:
    def __init__(self):
        self.router = APIRouter()
        self.configure_routes()

    def configure_routes(self):

        @self.router.get("/")
        def root():
            return {"message": "Hello from FastAPI, you are working"}

        @self.router.get("/status")
        def get_status():
            return {"status": "OK"}

    @inject
    async def _get_user_finance_data(
        self,
        userid: UserId = Body(...),
        data_service: DataService = Depends(Provide[Container.data_service]),
    ) -> Union[List[OperationOut], Response]:
        try:
            return data_service.get_user_operations(userid.user_id)
        except DataNotFound:
            return Response(status_code=status.HTTP_404_NOT_FOUND)

    def setup_injected_routes(self):
        self.router.add_api_route(
            path="/user/data",
            endpoint=self._get_user_finance_data,
            methods=["POST"],
            response_model=List[OperationOut]
        )