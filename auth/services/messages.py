from typing import Any
from pydantic import BaseModel
from pydantic import ConfigDict
from auth.services.messagebus import Messagebus

class Message(BaseModel):
    model_config = ConfigDict(frozen=True)

class Command(BaseModel):
    type: str
    payload: dict[str, Any]

class Query(BaseModel):
    type: str
    parameters: dict[str, Any]