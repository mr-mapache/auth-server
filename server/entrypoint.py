from contextlib import asynccontextmanager 
from fastapi import FastAPI  
from server.settings import Settings 
from server.connections import Database, Cache
from server.services.authentication import Authentication
from server.endpoints import authentication
from server.endpoints import forms
from server.middleware import SessionMiddleware
from authlib.integrations.starlette_client import OAuth

settings = Settings()
database = Database(settings)
cache = Cache(settings)  
oauth = OAuth(cache=cache) 
oauth.register(
    name='google',
    client_id=settings.google.client_id,
    client_secret=settings.google.client_secret.get_secret_value(),
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',  
    client_kwargs=settings.google.client_kwargs,
) 

@asynccontextmanager
async def lifespan(app):
    await database.setup()
    await cache.setup()
    try:
        yield
    finally:
        await database.teardown()
        await cache.teardown()

async def authentication_service() -> Authentication:
    return Authentication(oauth) 

api = FastAPI(lifespan=lifespan)
api.mount('/static', forms.static) 
api.include_router(forms.router)
api.include_router(authentication.router, prefix='/api')
api.dependency_overrides[authentication.service] = authentication_service

api.add_middleware(
    SessionMiddleware,
    secret_key=settings.sessions.secret_key
)