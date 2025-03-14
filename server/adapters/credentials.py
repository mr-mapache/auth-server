from typing import Protocol

from asyncio import to_thread 
from sqlalchemy.sql import insert, select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from passlib.context import CryptContext

from server.settings import Settings
from server.connections import Connections
from server.adapters.schemas import Username, Password, Owner

class Secret(Protocol):

    def get_secret_value() -> str | bytes:
        ...


def reveal(secret: Secret) -> str | bytes:
    return secret.get_secret_value()


class Cryptography:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.context = CryptContext(schemes=['bcrypt'])

    def verify(self, secret: Secret, hash: bytes) -> bool:
        return  self.context.verify(reveal(secret), hash)

    def hash(self, secret: Secret) -> bytes:
        hash = self.context.hash(reveal(secret))
        return hash.encode('utf-8')
    

class Credentials:
    def __init__(self, connections: Connections, settings: Settings, owner: Owner):
        self.connections = connections 
        self.owner = owner
        self.cryptography = Cryptography(settings)

    @property
    def sql(self) -> AsyncSession:
        return self.connections.sql
    
    async def add(self, username: Secret, password: Secret) -> None:
        command = insert(Username).values(value=reveal(username), user_pk=self.owner.id).returning(Username.pk)
        result = await self.sql.execute(command)
        username_pk = result.scalar()
        hash = await to_thread(self.cryptography.hash, password)
        command = insert(Password).values(hash=hash, username_pk=username_pk)
        await self.sql.execute(command)

    async def update(self, username: Secret, password: Secret) -> None:        
        command = update(Username).values(value=reveal(username), user_pk=self.owner.id).returning(Username.pk)
        result = await self.sql.execute(command)
        username_pk = result.scalar()
        hash = await to_thread(self.cryptography.hash, password)
        command = update(Password).where(username_pk==username_pk).values(hash=hash)
        await self.sql.execute(command)

    async def verify(self, username: Secret, password: Secret) -> bool:
        query = select(Password).join(Username).where(Username.value == reveal(username)).order_by(Password.created_at.desc()).limit(1)
        result = await self.sql.execute(query)
        secret = result.scalars().first()
        if not secret:
            return False 
        verified = await to_thread(self.cryptography.verify, password, secret.hash)
        return True if verified else False