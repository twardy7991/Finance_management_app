from fastapi import APIRouter, Depends, Response, status, Body, Form, UploadFile, File
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from app.endpoints.schemas import OperationConditions, OperationOut, CreateUserRequest, Token
from dependency_injector.wiring import Provide, inject
from app.database.repositories import DataNotFound, UserNotProvidedError
from typing import List, Union
from app.services.services import DataService, AuthenticationService
from app.containers import Container
from app.services.exceptions import TokenNotValidError
from jose import JWTError
import json
## we create funtion to point to the get_session from SQLconnection class so we can use it in Depends() 
## we create is outside the class as Depends() cannot use self.*** as it is in function parentheses

class Routing:
    def __init__(self):
        self.router = APIRouter()
        self.configure_routes()

    def configure_routes(self):

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
        except (TypeError, UserNotProvidedError) as e:
            return Response(
                content=json.dumps({"message" : "Nie udało się zapisać danych"}),
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                media_type="application/json"
                )
    
    @inject
    async def _register_user(
        self,
        user_request: CreateUserRequest = Body(...),
        auth_service : AuthenticationService = Depends(Provide[Container.auth_service])
    ) -> Response:
        try:
            auth_service.register_user(username=user_request.username, password=user_request.password)
        except Exception:
            return NotImplementedError 

    @inject
    async def _login_for_token(
        self,
        form_data : OAuth2PasswordRequestForm,
        auth_service : AuthenticationService = Depends(Provide[Container.auth_service])
    ): 
        token = auth_service.login_user(form_data.username, form_data.password)
        if not token:
            return Response(status_code=status.HTTP_401_UNAUTHORIZED)
        
        return {'access_token' : token, 'token_type' : 'bearer'}

    @inject
    async def _get_user(
        self,
        token : str = Depends(Provide[Container.oauth2_bearer]),
        auth_service : AuthenticationService = Depends(Provide[Container.auth_service])):
        
        try:
            username, user_id = auth_service.check_user_token(token=token)
            if username is not None and user_id is not None:
                return {'username' : username, 'id' : user_id}
            return Response(status_code=status.HTTP_401_UNAUTHORIZED) 
        
        except TokenNotValidError:
            return Response(status_code=status.HTTP_401_UNAUTHORIZED)
        
        except JWTError:
            return Response(status_code=status.HTTP_401_UNAUTHORIZED)
            
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
        
        self.router.add_api_route(
            path="/user/register",
            endpoint=self._register_user,
            methods=["POST"]
        )
        
        self.router.add_api_route(
            path="/user/token",
            endpoint=self._login_for_token,
            methods=["POST"],
            response_model=Token
        )
        
        self.router.add_api_route(
            path="/",
            endpoint=self._get_user,
            methods=["GET"], 
        )
        