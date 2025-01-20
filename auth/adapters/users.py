from uuid import UUID, uuid4
from typing import override
from typing import Optional
from dataclasses import dataclass
from sqlalchemy.sql import insert, select, update, delete

from auth.domain.users import Users as Repository
from auth.adapters.schemas import User, Email, Account
from auth.adapters.backend import UnitOfWork
from auth.adapters.emails import Emails
from auth.adapters.accounts import Accounts
from auth.adapters.sessions import Sessions

class Users(Repository):
    def __init__(self, uow: UnitOfWork):
        self.uow = uow
        self.emails = Emails(self.uow)
        self.accounts = Accounts(self.uow)
        self.sessions = Sessions(self.uow)

    @override
    async def create(self, id: UUID = None, name: Optional[str] = None) -> User:
        id = id or uuid4()
        command = insert(User).values(id=id, name=name).returning(User.pk)
        result = await self.uow.sql.execute(command)
        user_pk = result.scalar()
        user = User(pk=user_pk, id=id, name=name)
        user.emails = Emails(self.uow, user_pk=user_pk)
        user.accounts = Accounts(self.uow, user_pk=user_pk)
        user.sessions = Sessions(self.uow, user_id=user_pk)
        return user

    
    @override
    async def read(self, by: str, **kwargs) -> Optional[User]:
        match by:
            case 'id':
                query = select(User).where(User.id == kwargs['id'])

            case 'email':
                query = select(User).join(Email).where(Email.address == kwargs['address'])
            
            case 'account':
                query = select(User).join(Account).where(
                    Account.provider == kwargs['provider'],
                    Account.id == kwargs['id']
                )
            
            case 'session':
                async for key in self.uow.redis.scan_iter(match=f'*:{kwargs['id']}', count=1):
                    user_id = bytes(key).decode().split(':')[0]
                    query = select(User).where(User.id == user_id)

            case _:
                raise KeyError("Invalid query")

        result = await self.uow.sql.execute(query)
        user = result.scalars().first()
        if user:
            user.emails = Emails(self.uow, user_pk=user.pk)
            user.accounts = Accounts(self.uow, user_pk=user.pk)
            user.sessions = Sessions(self.uow, user_id=user.id)
            return user
        else:
            return None
                            
    @override
    async def update(self, id: UUID, name: Optional[str] = None) -> User:
        command = update(User).where(User.id == id).values(name=name).returning(User.pk)
        result = await self.uow.sql.execute(command)
        user_pk = result.scalar()
        user = User(pk=user_pk, id=id, name=name)
        user.emails = Emails(self.uow, user_pk=user_pk)
        user.accounts = Accounts(self.uow, user_pk=user_pk)
        user.sessions = Sessions(self.uow, user_id=user_pk)
        return user

    @override
    async def delete(self, id: UUID) -> None:
        command = delete(User).where(User.id == id)
        await self.uow.sql.execute(command)