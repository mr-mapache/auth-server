"""
While a RESTful API may seem convenient for creating a user by utilizing the POST /users/ endpoint
to generate a new user resource, the process of user registration often involves side effects that
extend beyond the scope of typical RESTful principles. Registration typically triggers actions such
as sending verification emails, generating authentication tokens, creating OAuth accounts initializing
user settings, or logging events. These actions are not simply resource manipulations but rather complex 
processes that involve multiple system interactions. That's why a registration service is necessary.
"""

from typing import Annotated 
from fastapi import FastAPI
from fastapi import Depends
from fastapi import Form
from fastapi import Response
from fastapi import status
from server.schemas import Shet
from server.services.registration import Registration

api = FastAPI()

async def service(*args, **kwargs) -> Registration:
    raise NotImplementedError("Override this dependency with a concrete implementation")

@api.post('/registration')
async def handle(form: Annotated[Shet, Form(...)], service: Annotated[Registration, Depends(service)]): 
    await service.handle(form)
    Response(status_code=status.HTTP_201_CREATED)













    