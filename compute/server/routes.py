from fastapi import APIRouter, Response, status, Body, Depends
from pydantic import BaseModel
from typing import List
from models import AbstractModel, LinearRegression
from services import ModelService
from typing import Annotated, Any
from containers import Container
from dependency_injector.wiring import inject, Provide
from exceptions import RegressionError

router = APIRouter()

class Coeff(BaseModel):
    coeff : List[int]
    free_val : int
    data_points : List[List[int]]
    
class Data(BaseModel):
    data : List[List]

@router.get('/status')
async def _status():
    return Response(status_code=status.HTTP_200_OK)

@router.post('/models/lr')
@inject
async def _compute_lr(
    model_service : Annotated[ModelService, Depends(Provide[Container.model_service])],
    data : Data = Body(...)
) -> dict[str, Any]:
    
    try:
        return  model_service.compute_lr(data=data.data)
    except RegressionError:
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        content="there was an error while processing")