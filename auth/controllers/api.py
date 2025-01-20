from contextlib import asynccontextmanager
from fastapi import FastAPI
from auth.adapters import Database, Cache, UnitOfWork
from auth.adapters.settings import Settings
from auth.adapters.users import Users
from auth.controllers import cqs

settings = Settings()
database = Database(settings)
cache = Cache(settings)

@asynccontextmanager
async def lifespan(*args, **kwargs):
    await database.setup(), await cache.setup()
    try:
        yield
    finally:
        await database.teardown(), await cache.teardown()

@asynccontextmanager
async def repository():
    async with UnitOfWork(database, cache) as uow:
        yield Users(uow)
        
api = FastAPI(lifespan=lifespan)
api.include_router(cqs.router)