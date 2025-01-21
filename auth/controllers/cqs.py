from typing import Annotated
from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Response, status
from auth.domain import Repository
from auth.services import Service
from auth.services import Command, Query
from auth.services.exceptions import HandlerNotFound

router = APIRouter()

async def repository() -> Repository:
    raise NotImplementedError("Override this dependency with a concrete implementation")

async def service() -> Service:
    raise NotImplementedError("Override this dependency with a concrete implementation")

@router.post('/commands/')
async def receive_command(request: Command, repository: Annotated[Repository, Depends(repository)], service: Annotated[Service, Depends(service)]):
    try:
        await service.execute(request.type, request.payload, repository)
        return Response(status_code=status.HTTP_202_ACCEPTED)    
    
    except HandlerNotFound as exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exception))    

@router.post('/queries/')
async def receive_query(request: Query, repository: Annotated[Repository, Depends(repository)], service: Annotated[Service, Depends(service)]):
    try:
        result = await service.execute(request.type, request.parameters, repository)
        return result
    
    except HandlerNotFound as exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exception))