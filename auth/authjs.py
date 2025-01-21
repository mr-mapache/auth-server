from contextlib import asynccontextmanager
from fastapi import FastAPI
from auth.adapters.backend import Database, Cache, Settings, UnitOfWork
from auth.adapters import Repository
from auth.controllers import cqs
from auth.services import authjs

settings = Settings()
database = Database()
cache = Cache()

@asynccontextmanager
async def lifespan():
    await database.setup()
    await cache.setup()
    try:
        yield
    finally:
        await cache.teardown()
        await database.teardown()

async def service():
    yield authjs.service

async def repository():
    async with UnitOfWork(database, cache) as uow:
        yield Repository(uow)

api = FastAPI(lifespan=lifespan)
api.include_router(cqs.router)
api.dependency_overrides[cqs.service] = service
api.dependency_overrides[cqs.repository] = repository