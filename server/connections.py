from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from sqlalchemy.ext.asyncio import AsyncConnection
from redis.asyncio import from_url, Redis
from server.settings import Settings 


class Database:
    engine: AsyncEngine
    connection: AsyncConnection

    def __init__(self, settings: Settings):
        self.engine = create_async_engine(url=settings.database.uri)
        
    async def setup(self):
        self.connection = await self.engine.connect()
        self.sessionmaker = async_sessionmaker(bind=self.connection, expire_on_commit=False)

    async def teardown(self):
        await self.connection.close()
        await self.engine.dispose()


class Cache:
    redis: Redis

    def __init__(self, settings: Settings):
        self.settings = settings

    async def setup(self):
        self.redis = await from_url(self.settings.cache.uri)

    async def teardown(self):
        await self.redis.aclose()

    async def flush(self):
        await self.redis.flushall()

 
class Connections:
    sql: AsyncSession

    def __init__(self, database: Database, cache: Cache):
        self.database = database
        self.cache = cache
    
    async def __aenter__(self):
        self.sql = self.database.sessionmaker()

        await self.sql.begin()
        return self
    
    async def __aexit__(self, exception_type, exception_value, traceback):
        if exception_type is not None:
            await self.sql.rollback()
        else:
            await self.sql.commit()
        await self.sql.close()