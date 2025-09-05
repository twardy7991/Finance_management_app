### FUNCTIONS THAT SET UP ROUTES ###

from typing import List, Union, Annotated
from datetime import date

from fastapi import APIRouter, Depends, Response, status, Body, Form, UploadFile, Header, File
from dependency_injector.wiring import Provide, inject
import json
from app.database.exceptions import DataNotFound, UserNotProvidedError 

from app.endpoints.schemes import Operation, CreateUserRequest, Data, Credentials, User, Session
from app.services import SessionService, ComputingService, DataService, UserService, AuthenticationService
from app.containers import Container
from app.services.exceptions import OperationsNotFoundError, PasswordIncorrectError, UsernameIncorrectError, DuplicateUsernameError

from app.endpoints.dependencies import get_current_user

router = APIRouter()

protected_router = APIRouter(
    #dependencies=[Depends(check_session)]
)

@router.get("/status")
async def _get_status():
    return {"status": "OK"}

@protected_router.get(
    path="/operations/chart", 
    tags=["operations"],
    response_model=Data
    )
@inject
async def _get_trend_data(
    computing_service : Annotated[ComputingService, Depends(Provide[Container.compute_service])],
    user_id : int = Depends(get_current_user)
)-> Response | Union[List[List[int]], List[int]]:  
    try:
        data : Data = computing_service.calculate_trend(user_id=user_id)
        return data
    except OperationsNotFoundError as e:
        return Response(status_code=status.HTTP_404_NOT_FOUND, content=str(e))

@protected_router.get(
    path="/operations/data",
    tags=["operations"],
    response_model=List[Operation]
    )
@inject
async def _get_user_finance_data(
    data_service: Annotated[DataService, Depends(Provide[Container.data_service])],
    user_id : int = Depends(get_current_user),
    date_from : date | None = None,
    date_to : date | None = None,
    order : str = "asc",
    operation_type : str | None = None,
    group_by : str | None = None
) -> Union[List[Operation], Response]:
    try:
        return data_service.get_user_operations(user_id=user_id, 
                                                date_from=date_from, 
                                                date_to=date_to,
                                                order=order,
                                                operation_type=operation_type,
                                                group_by=group_by)
    except DataNotFound as e:
        return Response(status_code=status.HTTP_404_NOT_FOUND, content=str(e))

@protected_router.post(
    path="/operations/upload",
    tags=["operations"]
    )
@inject
async def _post_user_finance_data(
    data_service: Annotated[DataService ,Depends(Provide[Container.data_service])],
    user_id : int = Depends(get_current_user),
    uploaded_file : UploadFile = File(...),
) -> Response:
    try:
        data_service.save_user_operations(user_id, uploaded_file.file)
        return Response(status_code=status.HTTP_201_CREATED)
    
    except (TypeError, UserNotProvidedError) as e:
        return Response(
            content=json.dumps({"message" : "Nie udało się zapisać danych"}),
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            media_type="application/json"
            )
    
@router.post(
        path="/user/register",
        tags=["user"]
)
@inject
async def _register_user(
    user_request: CreateUserRequest = Body(...),
    user_service : UserService = Depends(Provide[Container.user_service])
) -> Response:
    try:
        user_service.register_user(username=user_request.username, 
                                   password=user_request.password,
                                   name=user_request.name,
                                   surname=user_request.surname,
                                   telephone=user_request.telephone,
                                   address=user_request.address)
        return Response(status_code=status.HTTP_201_CREATED)
    except DuplicateUsernameError as e:
        return Response(status_code=status.HTTP_409_CONFLICT, content=str(e))
    except Exception:
        return NotImplementedError 

@protected_router.get(
    path="/user/profile",
    response_model=User,
    tags=["user"]
)
@inject
async def _get_user_profile_data(
    user_id : int = Depends(get_current_user),
    user_service : UserService = Depends(Provide[Container.user_service])
):
    try:
        return user_service.get_user(user_id=user_id)
    except Exception:
        raise NotImplementedError 

@router.post(
    "/user/login",
    tags=["user"],
    response_model=Session
)
@inject
async def _login(
    credentials : Credentials = Body(...),
    authentication_service : AuthenticationService = Depends(Provide[Container.auth_service]),
    session_service : SessionService = Depends(Provide[Container.session_service])
)-> Response:
    try:
        user_id = authentication_service.login_user(username=credentials.username,
                                          password=credentials.password)
        
        session_id = session_service.create_session(user_id=user_id)
        
        return {"session_id" : session_id}

    except PasswordIncorrectError as e:
        return Response(
            content=str(e),
            status_code=status.HTTP_401_UNAUTHORIZED
        )
    except UsernameIncorrectError as e:
        return Response(
            content=str(e),
            status_code=status.HTTP_401_UNAUTHORIZED
        )
    except Exception:
        raise NotImplementedError

@protected_router.post(
    path="/user/logout",
    tags=["user"]
)
@inject
async def _logout(
    user_id : int = Depends(get_current_user),
    session_service : SessionService = Depends(Provide[Container.session_service])
):
    session_service.delete_session(user_id=user_id)

@protected_router.patch(
    path="/user/update",
    tags=["user"]
)
@inject
async def _update_user(
    user_id : int = Depends(get_current_user),
    data : dict[str, str]  = Body(...),
    user_service : UserService = Depends(Provide[Container.user_service])
) -> Response:
    if user_service.update_user(user_id=user_id, data=data):
        return Response(status_code=status.HTTP_200_OK)
    return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)