from abc import ABC, abstractmethod
from typing import Protocol
from typing import Any
from datetime import datetime

class Session(Protocol):
    id: str
    payload: dict[str, Any]
    expires_at: datetime

class Sessions(ABC):
    """
    An abstract base class for a collection of sessions.
    """

    @abstractmethod
    def create(self, id: str, payload: dict[str, Any], expires_at: datetime) -> Session:...
    
    @abstractmethod
    async def put(self, session: Session):...

    @abstractmethod
    async def get(self, id: str) -> Session:...

    @abstractmethod
    async def remove(self, session: Session):...

    @abstractmethod
    async def list(self) -> list[Session]:...

    @abstractmethod
    async def clear(self):...