from abc import ABC, abstractmethod
from uuid import UUID
from typing import Optional
from dataclasses import dataclass
from auth.domain.ports import Emails, Accounts, Sessions

@dataclass
class User:
    id: UUID
    name: Optional[str]
    emails: Emails
    accounts: Accounts
    sessions: Sessions

class Repository(ABC):

    @abstractmethod
    async def create(self, id: UUID = None, name: Optional[str] = None) -> User:...

    @abstractmethod
    async def read(self, by: str, **kwargs) -> Optional[User]:...

    @abstractmethod
    async def update(self, id: UUID, **kwargs):...

    @abstractmethod
    async def delete(self, id: UUID):...