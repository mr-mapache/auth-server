from uuid import UUID, uuid4
from typing import override
from typing import Optional

from sqlalchemy.sql import insert, select, update, delete

from auth.adapters.schemas import User
from auth.adapters.schemas import Email
from auth.adapters.schemas import Account
from auth.adapters.setup import UnitOfWork
from auth.domain.ports import Users as Collection

class Users(Collection):
    def __init__(self, uow: UnitOfWork):
        self.uow = uow
    
    @override
    def create(self, id: UUID = None, name: Optional[str] = None) -> User:
        return User(id=id or uuid4(), name=name)

    @override
    async def add(self, user: User):
        command = insert(User).values(id=user.id, name=user.name).returning(User.pk)
        result = await self.uow.session.execute(command)
        user.pk = result.scalar()

    @override
    async def get(self, id: UUID) -> Optional[User]:
        query = select(User).where(User.id == id)
        result = await self.uow.session.execute(query)
        return result.scalars().first()

    @override
    async def get_by_email(self, address: str) -> Optional[User]:
        query = select(User).join(Email).where(Email.address == address)
        result = await self.uow.session.execute(query)
        return result.scalars().first()
    
    @override
    async def get_by_account(self, provider: str, id: str) -> Optional[User]:
        query = select(User).join(Account).where(Account.provider == provider, Account.id == id)
        result = await self.uow.session.execute(query)
        return result.scalars().first()
    
    @override
    async def get_by_session(self, id: UUID) -> Optional[User]:
        async for key in self.uow.redis.scan_iter(match=f'*:{id}', count=1):
            user_id = bytes(key).decode().split(':')[0]
            return await self.get(user_id)

    @override
    async def update(self, user: User):
        command = update(User).where(User.pk == user.pk).values(name=user.name)
        await self.uow.session.execute(command)
    
    @override
    async def remove(self, user: User):
        command = delete(User).where(User.pk == user.pk)
        await self.uow.session.execute(command)
        user.pk = None

