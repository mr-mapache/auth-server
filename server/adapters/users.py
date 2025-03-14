from uuid import UUID, uuid4 
from typing import Optional  

from sqlalchemy.sql import Executable
from sqlalchemy.sql import insert, select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from server.settings import Settings
from server.connections import Connections
from server.adapters.schemas import User, Username, Owner 
from server.adapters.sessions import Sessions
from server.adapters.credentials import reveal, Credentials
from server.adapters.emails import Emails, Email

class Users:
    def __init__(self, connections: Connections, settings: Settings):
        self.connections = connections
        self.settings = settings

    @property
    def sql(self) -> AsyncSession:
        return self.connections.sql

    async def create(self, id: UUID) -> User: 
        command = insert(User).values(id=id).returning(User.pk)
        result = await self.sql.execute(command)
        user_pk = result.scalar()
        user = User(pk=user_pk, id=id) 
        user.credentials = Credentials(self.connections, self.settings, Owner(id=user.pk))
        user.sessions = Sessions(self.connections, self.settings, Owner(id=user.id))
        user.emails = Emails(self.connections, self.settings, Owner(user.pk))
        return user
    
    async def read(self, by: str, **kwargs) -> Optional[User]: 
        user = None
        
        match by:
            case 'credentials':
                query = select(User).join(Username).where(Username.value == reveal(kwargs['username']))
                result = await self.sql.execute(query)
                user = result.scalars().first()

            case 'email':
                query = select(User).join(Email).where(Email.address == kwargs['address'])
                result = await self.sql.execute(query)
                user = result.scalars().first()

            case _:
                raise KeyError("Invalid query key")

        if user:
            user.credentials = Credentials(self.connections, self.settings, Owner(id=user.pk))
            user.sessions = Sessions(self.connections, self.settings, Owner(id=user.id))
            user.emails = Emails(self.connections, self.settings, Owner(user.pk))
            return user
        else:
            return None

    async def get(self, id: UUID) -> Optional[User]:
        query = select(User).where(User.id == id)
        result = await self.sql.execute(query)
        user = result.scalars().first()
        if user: 
            user.credentials = Credentials(self.connections, self.settings, Owner(id=user.pk))
            user.sessions = Sessions(self.connections, self.settings, Owner(id=user.id))
            user.emails = Emails(self.connections, self.settings, Owner(user.pk))
            return user
        else:
            return None

    async def delete(self, id: UUID) -> None:
        command = delete(User).where(User.id == id)
        await self.sql.execute(command)