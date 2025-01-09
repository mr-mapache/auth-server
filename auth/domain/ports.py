from abc import ABC, abstractmethod
from uuid import UUID
from typing import Optional
from typing import Any
from datetime import datetime
from auth.domain.models import User, Email, Account, Session

class Users(ABC):

    @abstractmethod
    def create(self, id: UUID = None, name: Optional[str] = None) -> User:...

    @abstractmethod
    async def add(self, user: User):...

    @abstractmethod
    async def get(self, id: UUID) -> Optional[User]:...

    @abstractmethod
    async def update(self, user: User):...

    @abstractmethod
    async def remove(self, id: UUID):...


class Accounts(ABC):

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


class Emails(ABC):

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


class Sessions(ABC):

    @abstractmethod
    def create(self, id: UUID, payload: dict[str, Any], expires_at: datetime) -> Session:...
    
    @abstractmethod
    async def put(self, session: Session):...

    @abstractmethod
    async def get(self, id: UUID) -> Session:...

    @abstractmethod
    async def remove(self, session: Session):...

    @abstractmethod
    async def list(self) -> list[Session]:...

    @abstractmethod
    async def clear(self):...