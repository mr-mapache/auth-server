from pytest_asyncio import fixture
from fastapi import FastAPI
from fastapi import Request
from httpx import AsyncClient, ASGITransport
from auth.services import authjs
from auth.endpoints import cqs

@fixture(scope='function')
async def authjs_client(users):
    async def repository(request: Request):
        assert request.headers['TenantID'] == 'Test'
        yield users

    api = FastAPI()
    api.include_router(cqs.router)
    api.dependency_overrides[cqs.repository] = repository
    api.dependency_overrides[cqs.service] = lambda: authjs.service
    async with AsyncClient(transport=ASGITransport(api), base_url='http://testserver') as client:
        yield client