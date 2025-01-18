from typing import Annotated
from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Response, status
from auth.services import Service
from auth.services import Command, Query
from auth.services.exceptions import HandlerNotFound

router = APIRouter()

async def port() -> Service:
    raise NotImplementedError("Override this dependency with a concrete implementation")

@router.post('/commands/')
async def handle_command(request: Command, service: Annotated[Service, Depends(port)]):
    try:
        await service.execute(request.type, request.payload)
        return Response(status_code=status.HTTP_202_ACCEPTED)    
    
    except HandlerNotFound as exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exception))
    

@router.post('/queries/')
async def handle_query(request: Query, service: Annotated[Service, Depends(port)]):
    try:
        result = await service.execute(request.type, request.parameters)
        return result
    
    except HandlerNotFound as exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exception))
    
