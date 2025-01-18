from abc import ABC, abstractmethod
from typing import Protocol
from typing import Optional

class Account(Protocol):
    id: str
    type: str
    provider: str

class Accounts(ABC):
    """
    An abstract base class for a collection of accounts.
    """

    @abstractmethod
    def create(self, type: str, provider: str, id: str) -> Account:...

    @abstractmethod
    async def add(self, account: Account):...

    @abstractmethod
    async def get(self, provider: str, id: str) -> Optional[Account]:...

    @abstractmethod
    async def list(self) -> list[Account]:...

    @abstractmethod
    async def remove(self, account: Account):...