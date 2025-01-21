from asyncio import run
from pytest_asyncio import fixture
from fastapi import FastAPI
from httpx import AsyncClient, ASGITransport
from auth.controllers import cqs
from auth.services import authjs

@fixture(scope='function')
async def authjs_service(users):
    async def repository():
        yield users
        
    authjs.service.dependency_overrides[authjs.port] = repository
    return authjs.service

@fixture(scope='function')
async def authjs_client(users):
    api = FastAPI()
    api.include_router(cqs.router)
    api.dependency_overrides[cqs.repository] = lambda: users
    api.dependency_overrides[cqs.service] = lambda: authjs.service
    async with AsyncClient(transport=ASGITransport(api), base_url='http://testserver') as client:
        yield client