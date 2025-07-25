from app.endpoints.schemas import OperationConditions, OperationOut, CreateUserRequest, Token, Data
from app.database.repositories import DataNotFound, UserNotProvidedError
from app.services.compute_service import ComputingService
from app.services.data_service import DataService
from app.services.authentication_services import AuthenticationService
from app.containers import Container
from app.services.exceptions import TokenNotValidError, OperationsNotFoundError

from fastapi import APIRouter, Depends, Response, status, Body, Form, UploadFile, File
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from dependency_injector.wiring import Provide, inject
from typing import List, Union, Annotated
from jose import JWTError
import json

router = APIRouter()

@router.get("/status")
async def _get_status():
    return {"status": "OK"}

@router.get(
    path="/chart", 
    response_model=Data
    )
@inject
async def _calculate_trend(
    computing_service : Annotated[ComputingService, Depends(Provide[Container.compute_service])],
    conditions : OperationConditions = Body(...)
):  
    try:
        data : Data = computing_service.calculate_trend(user_id=conditions.user_id)
        return data
    except OperationsNotFoundError as e:
        return Response(status_code=status.HTTP_404_NOT_FOUND, content=str(e))

@router.post(
    path="/user/data",
    response_model=List[OperationOut]
    )
@inject
async def _get_user_finance_data(
    data_service: Annotated[DataService, Depends(Provide[Container.data_service])],
    body_params: OperationConditions = Body(...),
) -> Union[List[OperationOut], Response]:
    try:
        return data_service.get_user_operations(body_params.user_id, body_params.date_from, body_params.date_to)
    except DataNotFound:
        return Response(status_code=status.HTTP_404_NOT_FOUND)

@router.post(
    path="/user/upload",
    )
@inject
async def _post_user_finance_data(
    data_service: Annotated[DataService ,Depends(Provide[Container.data_service])],
    user_id : int = Form(...),
    uploaded_file : UploadFile = Form(...),
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
    
    # @inject
    # async def _register_user(
    #     self,
    #     user_request: CreateUserRequest = Body(...),
    #     auth_service : AuthenticationService = Depends(Provide[Container.auth_service])
    # ) -> Response:
    #     try:
    #         auth_service.register_user(username=user_request.username, password=user_request.password)
    #     except Exception:
    #         return NotImplementedError 

    # # @inject
    # async def _login_for_token(
    #     self,
    #     form_data : OAuth2PasswordRequestForm,
    #     auth_service : AuthenticationService = Depends(Provide[Container.auth_service])
    # ): 
    #     token = auth_service.login_user(form_data.username, form_data.password)
    #     if not token:
    #         return Response(status_code=status.HTTP_401_UNAUTHORIZED)
        
    #     return {'access_token' : token, 'token_type' : 'bearer'}

    # @inject
    # async def _get_user(
    #     self,
    #     token : str = Depends(Provide[Container.oauth2_bearer]),
    #     auth_service : AuthenticationService = Depends(Provide[Container.auth_service])):
        
    #     try:
    #         username, user_id = auth_service.check_user_token(token=token)
    #         if username is not None and user_id is not None:
    #             return {'username' : username, 'id' : user_id}
    #         return Response(status_code=status.HTTP_401_UNAUTHORIZED) 
        
    #     except TokenNotValidError:
    #         return Response(status_code=status.HTTP_401_UNAUTHORIZED)
        
    #     except JWTError:
    #         return Response(status_code=status.HTTP_401_UNAUTHORIZED)
      
    #     self.router.add_api_route(
    #         path="/user/register",
    #         endpoint=self._register_user,
    #         methods=["POST"]
    #     )
        
        # self.router.add_api_route(
        #     path="/user/token",
        #     endpoint=self._login_for_token,
        #     methods=["POST"],
        #     response_model=Token
        # )
        
        # self.router.add_api_route(
        #     path="/",
        #     endpoint=self._get_user,
        #     methods=["GET"], 
        # )
        