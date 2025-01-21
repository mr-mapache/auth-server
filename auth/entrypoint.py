from contextlib import asynccontextmanager
from fastapi import FastAPI
from auth.adapters import Database, Cache, Settings
from auth.middleware import CORSMiddleware

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
        await cache.teardown()
        await database.teardown()

app = FastAPI(root_path='/api', lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)