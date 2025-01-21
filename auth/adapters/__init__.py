from contextlib import asynccontextmanager
from auth.adapters.backend import Database as Database
from auth.adapters.backend import Cache as Cache
from auth.adapters.backend import UnitOfWork as UnitOfWork
from auth.settings import Settings as Settings
from auth.adapters.users import Users as Users

settings = Settings()
database = Database(settings)
cache = Cache(settings)

@asynccontextmanager
async def lifespan(*args, **kwargs):
    await database.setup()
    await cache.setup()
    try:
        yield
    finally:
        await cache.teardown()
        await database.teardown()