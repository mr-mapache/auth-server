from typing import Protocol

from asyncio import to_thread 
from sqlalchemy.sql import insert, select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from bcrypt import checkpw, hashpw, gensalt 

from server.settings import Settings
from server.connections import UnitOfWork
from server.adapters.schemas import User, Password, Owner

class Secret(Protocol):

    def get_secret_value() -> str | bytes:
        ...

def reveal(secret: Secret) -> str | bytes:
    if isinstance(secret, str):
        return secret
    else:
        return secret.get_secret_value()

class Cryptography:
    def __init__(self, settings: Settings):
        self.settings = settings

    async def verify(self, secret: Secret, hash: bytes) -> bool:
        return await to_thread(checkpw, reveal(secret), hash) 

    async def hash(self, secret: Secret) -> bytes: 
        return await to_thread(hashpw, reveal(secret), gensalt())
    

class Credentials:
    def __init__(self, uow: UnitOfWork, settings: Settings, owner: Owner):
        self.uow = uow 
        self.owner = owner
        self.cryptography = Cryptography(settings)

    @property
    def sql(self) -> AsyncSession:
        return self.uow.sql
    
    async def put(self, password: Secret) -> None:  
        hash = await self.cryptography.hash(password) 
        command = (
            insert(Password).
            values(hash=hash, user_pk=self.owner.id)
        )
        await self.sql.execute(command)
 
    async def verify(self, username: Secret, password: Secret) -> bool: 
        query = (
            select(Password).
            join(User).
            where(User.username == reveal(username)).
            where(Password.is_active == True).
            order_by(Password.pk.desc()).
            limit(1)
        )
        result = await self.sql.execute(query)
        secret = result.scalars().first()  
        if not secret:
            return False   
        verified = await self.cryptography.verify(password, secret.hash)
        return True if verified else False