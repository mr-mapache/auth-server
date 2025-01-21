from auth.domain import Users
from auth.services import Service

async def users() -> Users:
    raise NotImplementedError("Override this dependency with a concrete implementation")

async def service() -> Service:
    raise NotImplementedError("Override this dependency with a concrete implementation")