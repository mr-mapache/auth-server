from typing import Annotated

from fastapi import APIRouter
from fastapi import Request
from fastapi import Depends
from fastapi import Path  
from fastapi import Query
from server.services.authentication import Authentication

router = APIRouter()

async def service() -> Authentication:
    ...

@router.get("/auth/{provider}/callback")
async def callback(request: Request, provider: Annotated[str, Path(...)], service: Annotated[Authentication, Depends(service)]): 
    return await service.callback(request, provider)

@router.get('/auth/{provider}/login')
async def login(request: Request, provider: Annotated[str, Path(...)], state: Annotated[str, Query(...)], service: Annotated[Authentication, Depends(service)]):
    return await service.redirect(request, provider, state)