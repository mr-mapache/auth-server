from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import async_sessionmaker
from redis.asyncio import from_url
from auth.settings import Settings

class Database:
    def __init__(self, settings: Settings):
        self.engine = create_async_engine(url=settings.database.uri)
        
    async def setup(self):
        self.connection = await self.engine.connect()
        self.sessionmaker = async_sessionmaker(bind=self.connection)

    async def teardown(self):
        await self.connection.close()
        await self.engine.dispose()


class Cache:
    def __init__(self, settings: Settings):
        self.settings = settings

    async def setup(self):
        self.redis = await from_url(self.settings.cache.uri)

    async def teardown(self):
        await self.redis.aclose()

    async def flush(self):
        await self.redis.flushall()


class UnitOfWork:
    def __init__(self, database: Database, cache: Cache):
        self.database = database
        self.cache = cache
    
    async def __aenter__(self):
        self.sql = self.database.sessionmaker()
        self.redis = self.cache.redis
        await self.sql.begin()
        return self
    
    async def __aexit__(self, exception_type, exception_value, traceback):
        if exception_type is not None:
            await self.sql.rollback()
        else:
            await self.sql.commit()
        await self.sql.close()
