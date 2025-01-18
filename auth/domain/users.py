from abc import ABC, abstractmethod
from uuid import UUID
from typing import Optional
from typing import Protocol
from auth.domain.accounts import Accounts
from auth.domain.emails import Emails
from auth.domain.sessions import Sessions

class User(Protocol):
    """
    A user entitiy representing the aggregate root of the user's domain.
    """

    id: UUID
    name: Optional[str]
    emails: Emails
    accounts: Accounts
    sessions: Sessions

class Users(ABC):
    """
    An abstract base class for the repository of users.
    """

    @abstractmethod
    async def create(self, id: UUID = None, name: Optional[str] = None) -> User:...

    @abstractmethod
    async def read(self, by: str, **kwargs) -> Optional[User]:...

    @abstractmethod
    async def update(self, id: UUID, **kwargs) -> User:...

    @abstractmethod
    async def delete(self, id: UUID):...