from uuid import UUID, uuid4 
from typing import Optional  
 
from sqlalchemy.sql import insert, select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from server.settings import Settings
from server.connections import UnitOfWork
from server.adapters.schemas import User, Owner 
from server.adapters.sessions import Sessions
from server.adapters.credentials import reveal, Secret, Credentials
from server.adapters.emails import Emails, Email

class Users:
    def __init__(self, uow: UnitOfWork, settings: Settings):
        self.uow = uow
        self.settings = settings

    @property
    def sql(self) -> AsyncSession:
        return self.uow.sql

    async def create(self, id: UUID, username: Optional[str | Secret] = None) -> User: 
        command = (
            insert(User).
            values(id=id, username=reveal(username) if username else None).
            returning(User)
        )
        result = await self.sql.execute(command)
        user = result.scalars().first()
        user.credentials = Credentials(self.uow, self.settings, Owner(id=user.pk))
        user.sessions = Sessions(self.uow, self.settings, Owner(id=user.id))
        user.emails = Emails(self.uow, self.settings, Owner(user.pk))
        return user
    
    async def read(self, by: str, **kwargs) -> Optional[User]: 
        user = None

        match by:
            case 'credentials':
                query = (
                    select(User).
                    where(User.username == reveal(kwargs['username']))
                )
                result = await self.sql.execute(query)
                user = result.scalars().first()

            case 'email':
                query = (
                    select(User).
                    join(Email).
                    where(Email.address == kwargs['address'])
                )
                result = await self.sql.execute(query)
                user = result.scalars().first()

            case _:
                raise KeyError("Invalid query key")

        if user:
            user.credentials = Credentials(self.uow, self.settings, Owner(id=user.pk))
            user.sessions = Sessions(self.uow, self.settings, Owner(id=user.id))
            user.emails = Emails(self.uow, self.settings, Owner(user.pk))
            return user
        else:
            return None

    async def get(self, id: UUID) -> Optional[User]:
        query = (
            select(User).
            where(User.id == id)
        )
        result = await self.sql.execute(query)
        user = result.scalars().first()
        if user: 
            user.credentials = Credentials(self.uow, self.settings, Owner(id=user.pk))
            user.sessions = Sessions(self.uow, self.settings, Owner(id=user.id))
            user.emails = Emails(self.uow, self.settings, Owner(user.pk))
            return user
        else:
            return None
        
    async def update(self, id: UUID, username: str | Secret | None): 
        command = (
            update(User).
            values(username=reveal(username) if username else None).
            where(User.id == id)
        )
        await self.sql.execute(command) 
        

    async def delete(self, id: UUID) -> None:
        command = (
            delete(User).
            where(User.id == id)
        )
        await self.sql.execute(command)