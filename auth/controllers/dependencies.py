from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi import Request
from auth.settings import Settings
from auth.adapters.setup import Database, Cache, UnitOfWork
from auth.adapters.repository import Repository

settings = Settings()
database = Database(settings)
cache = Cache(settings)

@asynccontextmanager
async def lifespan(api: FastAPI):
    await database.setup(), await cache.setup()
    try:
        yield
    finally:
        await database.teardown(), await cache.teardown()

@asynccontextmanager
async def repository_adapter():
    async with UnitOfWork(database, cache) as uow:
        yield Repository(uow)