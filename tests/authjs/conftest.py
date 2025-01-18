from asyncio import run
from pytest_asyncio import fixture
from fastapi import FastAPI
from httpx import AsyncClient, ASGITransport
from auth.controllers import cqs
from auth.services import authjs

@fixture(scope='function')
async def authjs_service(users):
    authjs.service.dependency_overrides[authjs.port] = lambda: users
    return authjs.service

@fixture(scope='function')
async def authjs_client(authjs_service):
    api = FastAPI()
    api.include_router(cqs.router)
    api.dependency_overrides[cqs.port] = lambda: authjs_service
    async with AsyncClient(transport=ASGITransport(api), base_url='http://testserver') as client:
        yield client