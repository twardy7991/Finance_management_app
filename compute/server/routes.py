from typing import List, Annotated, Any

from fastapi import APIRouter, Response, status, Body, Depends
from pydantic import BaseModel
from dependency_injector.wiring import inject, Provide

from services import ModelService
from containers import Container
from exceptions import RegressionError



## models for routes

class Coeff(BaseModel):
    coeff : List[int]
    free_val : int
    data_points : List[List[int]]
    
class Data(BaseModel):
    data : List[List]

## routes configuration
router = APIRouter()

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