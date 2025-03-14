from collections.abc import Callable
from uuid import uuid4
from typing import Awaitable
 
from server.ports.users import User, Users
from server.schemas import Shet 


async def validate_credentials(shet: Shet, users: Users):
    if shet.username and not shet.password:
        raise Exception("Cannot register a user with username without a password")

    if not shet.username and not shet.password:
        raise Exception("Cannot register a user with password without a username")
    
    if shet.username and shet.password:
        if await users.read(by='credentials', username=shet.username):
            raise Exception("Username already exists") 


async def validate_email_address(shet: Shet, users: Users):
    if shet.email and await users.read(by='email', address = shet.email):
        raise Exception("Email address already exists")


class Validation:
    def __init__(self, users: Users):
        self.users = users
        self.handlers = list[Callable[[Shet, Users], Awaitable[None]]]([
            validate_credentials,
            validate_email_address
        ])

    async def handle(self, payload: Shet) -> None: 
        for handler in self.handlers:
            await handler(payload, self.users)


class Registration:
    def __init__(self, users: Users):
        self.users = users
        self.validation = Validation(users)

    async def handle(self, payload: Shet)-> User: 
        await self.validation.handle(payload)

        user = await self.users.create(id=uuid4())        
        
        if payload.username and payload.password:
            await user.credentials.add(payload.username, payload.password)

        if payload.email:
            await user.emails.add(payload.email, primary=True, verified=False)
        
        return user





        