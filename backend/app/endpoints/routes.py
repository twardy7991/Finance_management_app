from fastapi import APIRouter, Depends, Response, status, Body, Form, UploadFile, File
from app.endpoints.schemas import OperationConditions, OperationOut
from dependency_injector.wiring import Provide, inject
from app.database.repositories import DataNotFound
from typing import Annotated, List, Union
from app.services.services import DataService
from app.containers import Container
import json
import pandas as pd
## we create funtion to point to the get_session from SQLconnection class so we can use it in Depends() 
## we create is outside the class as Depends() cannot use self.*** as it is in function parentheses

class Routing:
    def __init__(self):
        self.router = APIRouter()
        self.configure_routes()

    def configure_routes(self):

        @self.router.get("/")
        def _root():
            return {"message": "Hello from FastAPI, you are working"}

        @self.router.get("/status")
        def _get_status():
            return {"status": "OK"}

    ## setted up injected routes with two methods due to errors
    @inject
    async def _get_user_finance_data(
        self,
        body_params: OperationConditions = Body(...),
        data_service: DataService = Depends(Provide[Container.data_service]),
    ) -> Union[List[OperationOut], Response]:
        try:
            return data_service.get_user_operations(body_params.user_id, body_params.date_from, body_params.date_to)
        except DataNotFound:
            return Response(status_code=status.HTTP_404_NOT_FOUND)

    @inject
    async def _post_user_finance_data(
        self,
        user_id : int = Form(...),
        uploaded_file : UploadFile = File(...),
        data_service: DataService = Depends(Provide[Container.data_service])
    ) -> Response:
        try:
            data_service.save_user_operations(user_id, uploaded_file.file)
            return Response(status_code=status.HTTP_200_OK)
        except TypeError as e:
            return Response(
                content=json.dumps({"message" : "Nie udało się zapisać danych"}),
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                media_type="application/json"
                )

    def setup_injected_routes(self):
        self.router.add_api_route(
            path="/user/data",
            endpoint=self._get_user_finance_data,
            methods=["POST"],
            response_model=List[OperationOut]
        )
        
        self.router.add_api_route(
            path="/user/upload",
            endpoint=self._post_user_finance_data,
            methods=["POST"],
        )
        