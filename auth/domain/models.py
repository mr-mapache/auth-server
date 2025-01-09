from uuid import UUID
from typing import Protocol
from typing import Optional
from typing import Any
from datetime import datetime

class User(Protocol):
    id: UUID
    name: Optional[str]

class Account(Protocol):
    id: str
    type: str
    provider: str

class Email(Protocol):
    address: str
    is_verified: bool
    is_primary: bool
    verified_at: datetime

class Session(Protocol):
    id: UUID
    payload: dict[str, Any]
    expires_at: datetime
