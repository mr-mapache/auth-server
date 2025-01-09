from fastapi import FastAPI
from fastapi import Request, status
from fastapi import HTTPException
from auth.services.exceptions import (
    NotFoundError,
    AlreadyExistsError
)
from auth.controllers.dependencies import settings
from auth.controllers.dependencies import lifespan

api = FastAPI(root_path=settings.api.root_path, lifespan=lifespan)

@api.exception_handler(NotFoundError)
async def not_found_error_handler(request: Request, exception: NotFoundError):
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=exception.message)

@api.exception_handler(AlreadyExistsError)
async def already_exists_error_handler(request: Request, exception: AlreadyExistsError):
    raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=exception.message)