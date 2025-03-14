from contextlib import asynccontextmanager
from fastapi import FastAPI
from server.settings import Settings 
from server.connections import Database, Cache

settings = Settings()
database = Database(settings)
cache = Cache(settings) 

@asynccontextmanager
async def lifespan(app):
    await database.setup()
    await cache.setup()
    try:
        yield
    finally:
        await database.teardown()
        await cache.teardown()

api = FastAPI(lifespan=lifespan)