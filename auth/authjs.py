from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi import Request
from fastapi import HTTPException, status
from auth.adapters import Users
from auth.adapters import Database, Cache, Settings, UnitOfWork
from auth.controllers.routers import cqs
from auth.services import authjs
from auth.services.authjs.exceptions import (
    AccountNotFound,
    EmailAlreadyExists,
    EmailNotFound,
    SessionNotFound,
    UserAlreadyExists,
    UserNotFound
)

settings = Settings()
database = Database(settings)
cache = Cache(settings)

@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.setup()
    await cache.setup()
    try:
        yield
    finally:
        await cache.teardown()
        await database.teardown()

async def authjs_service():
    yield authjs.service

async def users_repository():
    async with UnitOfWork(database, cache) as uow:
        yield Users(uow)

async def handle_not_found_exception(request: Request, exception: Exception):
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=str(exception)
    )

async def handle_already_exists_exception(request: Request, exception: Exception):
    return HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail=str(exception)
    )

app = FastAPI(lifespan=lifespan)
app.include_router(cqs.router)
app.add_exception_handler(UserNotFound, handle_not_found_exception)
app.add_exception_handler(AccountNotFound, handle_not_found_exception)
app.add_exception_handler(EmailNotFound, handle_not_found_exception)
app.add_exception_handler(SessionNotFound, handle_not_found_exception)
app.add_exception_handler(EmailAlreadyExists, handle_already_exists_exception)
app.add_exception_handler(UserAlreadyExists, handle_already_exists_exception)
app.dependency_overrides[cqs.service] = authjs_service
app.dependency_overrides[cqs.repository] = users_repository

if __name__ == '__main__':
    from uvicorn import run
    from controllers import transport
    
    transport.app.mount('/authjs', app, name='AuthJS')
    run(transport.app, host='0.0.0.0', port=8000)