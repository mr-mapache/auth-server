from pytest import fixture
from fastapi import FastAPI
from httpx import AsyncClient, ASGITransport

from auth.controllers.routers import cqs
from auth.controllers.api import api
from auth.services.authjs.handlers import messagebus, repository_port

@fixture
async def messagebus_adapter(repository):
    messagebus.dependency_overrides[repository_port] = lambda: repository
    return messagebus

@fixture
async def nextauth_client(messagebus_adapter):
    api.include_router(cqs.router)
    api.dependency_overrides[cqs.messagebus_port] = lambda: messagebus_adapter
    async with AsyncClient(transport=ASGITransport(api), base_url='http://testserver/cqrs') as client:
        yield client