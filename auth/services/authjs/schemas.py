from uuid import UUID
from typing import Annotated, Optional
from datetime import datetime
from pydantic import BaseModel
from pydantic import Field
from pydantic import EmailStr
from pydantic import ConfigDict

class Schema(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

class User(Schema):    
    id: Annotated[Optional[UUID], Field(alias='id')]
    name: Annotated[str, Field(alias='name')]
    email_address: Annotated[EmailStr, Field(alias='email')]
    email_verified_at: Annotated[Optional[datetime], Field(alias='emailVerified')]
    profile_image: Annotated[Optional[str], Field(alias='image')]

class Session(Schema):
    id: Annotated[Optional[UUID], Field(alias='sessionToken')]
    expires_at: Annotated[datetime, Field(alias='expires')]

class Account(Schema):
    id: Annotated[str, Field(..., validation_alias='providerAccountId')]
    type: Annotated[str, Field(..., validation_alias ='type')]
    provider: Annotated[str, Field(..., validation_alias='provider')]
    access_token: Annotated[str, Field(...)]
    token_type: Annotated[str, Field(...)]
    expires_in: Annotated[Optional[int], Field(default=None)]
    id_token: Annotated[Optional[str], Field(default=None)]
    refresh_token: Annotated[Optional[str], Field(default=None)]
    scope: Annotated[Optional[str], Field(default=None)]