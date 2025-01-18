from contextlib import asynccontextmanager
from fastapi import FastAPI
from auth.adapters import Database, Cache, UnitOfWork
from auth.adapters.settings import Settings
from auth.adapters.users import Users
from auth.services import authjs
from auth.controllers import cqs
from auth.controllers.middleware import CORSMiddleware

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
        
authjs.service.dependency_overrides[authjs.port] = repository
api = FastAPI(lifespan=lifespan)
api.dependency_overrides[cqs.service] = lambda: authjs.service
api.include_router(cqs.router)
api.add_middleware(CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)