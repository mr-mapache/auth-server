from pytest_asyncio import fixture 
from fastapi import FastAPI
from httpx import AsyncClient, ASGITransport
from server.settings import Settings
from server.connections import Database, Cache, Connections
from server.adapters.schemas import Schema
from server.adapters.users import Users  
from dotenv import load_dotenv

load_dotenv()

@fixture(scope='session')
def settings() -> Settings:
    return Settings()

@fixture(scope='function')
async def database(settings: Settings):
    database = Database(settings)
    await database.setup()
    transaction = await database.connection.begin()
    await database.connection.run_sync(Schema.metadata.create_all)
    try:
        yield database
    finally:
        await transaction.rollback()
        await database.connection.run_sync(Schema.metadata.drop_all)
        await database.teardown()


@fixture(scope='function')
async def cache(settings: Settings):
    cache = Cache(settings)
    await cache.setup()
    try:
        yield cache
    finally:
        await cache.flush()
        await cache.teardown()
 

@fixture(scope='function')
async def connections(database: Database, cache: Cache):
    async with Connections(database, cache) as connections:
        yield connections


@fixture(scope='function')
async def users(connections: Connections, settings: Settings):
    return Users(connections, settings)


#@fixture(scope='function')
#async def client(users: Users, settings: Settings):  
#    api = FastAPI()
#    api.include_router(authentication.router) 
#    api.dependency_overrides[authentication.service] = lambda: Authentication(users, settings)
#    async with AsyncClient(transport=ASGITransport(api), base_url='http://testserver') as client:
#        yield client