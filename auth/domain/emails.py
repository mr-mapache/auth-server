from abc import ABC, abstractmethod
from typing import Optional
from typing import Protocol
from datetime import datetime

class Email(Protocol):
    address: str
    is_primary: bool
    verified_at: datetime

    @property
    def is_verified(self) -> bool:...


class Emails(ABC):
    """
    An abstract base class for a collection of emails.
    """

    @abstractmethod
    def create(self, address: str, is_primary: bool, is_verified: bool, verified_at: datetime | None = None) -> Email:...

    @abstractmethod
    async def add(self, email: Email):...

    @abstractmethod
    async def get(self, address: str) -> Optional[Email]:...

    @abstractmethod
    async def update(self, email: Email):...

    @abstractmethod
    async def list(self) -> list[Email]:...

    @abstractmethod
    async def remove(self, email: Email):...