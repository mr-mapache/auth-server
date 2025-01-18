from uuid import UUID
from datetime import datetime
from typing import Annotated
from typing import Optional
from pydantic import BaseModel
from pydantic import Field
from pydantic import EmailStr

class Command(BaseModel):...

class CreateUser(Command):
    user_id: Annotated[UUID, Field(..., validation_alias ='id')]
    user_name: Annotated[str, Field(..., validation_alias ='name')]
    user_email_address: Annotated[EmailStr, Field(..., validation_alias ='email')]
    user_email_verified_at: Annotated[Optional[datetime], Field(..., validation_alias ='emailVerified')]
    user_profile_image: Annotated[Optional[str], Field(..., validation_alias ='image')]

class UpdateUser(Command):
    user_id: Annotated[UUID, Field(..., validation_alias ='id')]
    user_name: Annotated[Optional[str], Field(..., validation_alias ='name')]
    user_email_address: Annotated[Optional[EmailStr], Field(..., validation_alias ='email')]
    user_email_verified_at: Annotated[Optional[datetime], Field(..., validation_alias ='emailVerified')]
    user_image: Annotated[Optional[str], Field(..., validation_alias ='image')]

class DeleteUser(Command):
    user_id: Annotated[UUID, Field(..., validation_alias ='id')]

class LinkAccount(Command):
    user_id: Annotated[UUID, Field(..., validation_alias ='userId')]
    account_id: Annotated[str, Field(..., validation_alias='providerAccountId')]
    account_type: Annotated[str, Field(..., validation_alias ='type')]
    account_provider: Annotated[str, Field(..., validation_alias='provider')]
    access_token: Annotated[str, Field(...)]
    token_type: Annotated[str, Field(...)]
    expires_in: Annotated[Optional[int], Field(default=None)]
    id_token: Annotated[Optional[str], Field(default=None)]
    refresh_token: Annotated[Optional[str], Field(default=None)]
    scope: Annotated[Optional[str], Field(default=None)]

class UnlinkAccount(Command):
    account_id: Annotated[str, Field(..., validation_alias='providerAccountId')]
    account_provider: Annotated[str, Field(..., validation_alias='provider')]

class CreateSession(Command):
    session_id: Annotated[str, Field(..., validation_alias='sessionToken')]
    user_id: Annotated[str, Field(..., validation_alias='userId')]
    expires_at: Annotated[datetime, Field(..., validation_alias='expires')]

class UpdateSession(Command):
    session_id: Annotated[str, Field(..., validation_alias='sessionToken')]
    expires_at: Annotated[Optional[datetime], Field(..., validation_alias='expires')]

class DeleteSession(Command):
    session_id: Annotated[str, Field(..., validation_alias='sessionToken')]