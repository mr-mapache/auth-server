from uuid import UUID
from pydantic import EmailStr
from pydantic import BaseModel
from pydantic import Field

class Query(BaseModel):...

class GetUserById(Query):
    user_id: UUID = Field(..., validation_alias='id')

class GetUserByEmail(Query):
    email_address: EmailStr = Field(..., validation_alias='email')

class GetUserByAccount(Query):
    account_provider: str = Field(..., validation_alias='provider')
    account_id: str = Field(..., validation_alias='providerAccountId')

class GetSessionAndUser(Query):
    session_id: str = Field(..., validation_alias='sessionToken')