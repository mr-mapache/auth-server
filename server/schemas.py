from uuid import UUID
from typing import Any
from typing import Literal
from typing import Annotated
from typing import Optional
from pydantic import BaseModel
from pydantic import SecretStr
from pydantic import SecretBytes 
from pydantic import EmailStr
from pydantic import Field
 
class Schema(BaseModel):...

class User(Schema):
    id: Annotated[UUID, Field(...)]

class Credentials(Schema):
    username: Annotated[SecretStr, Field(...)]
    password: Annotated[SecretBytes, Field(...)] 

class Token(Schema):
    access_token: Annotated[str, Field(...)]
    token_type: Annotated[Literal['Bearer', 'MAC'], Field(...)]

class Shet(Schema):
    email: Annotated[Optional[EmailStr], Field(default=None)]
    username: Annotated[Optional[SecretStr], Field(default=None)]
    password: Annotated[Optional[SecretBytes], Field(default=None)]