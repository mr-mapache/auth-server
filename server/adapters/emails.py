from typing import Optional 
from typing import Optional  
 
from sqlalchemy.sql import insert, select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from server.settings import Settings
from server.connections import Connections
from server.adapters.schemas import Owner
from server.adapters.schemas import Owner, Email

class Emails:
    def __init__(self, connections: Connections, settings: Settings, owner: Owner):
        self.connections = connections
        self.settings = settings
        self.owner = owner

    @property
    def sql(self) -> AsyncSession:
        return self.connections.sql
     
    async def add(self, address: str, primary: bool, verified: bool): 
        if primary:
            command = (
                update(Email).
                where(Email.user_pk == self.owner.id, Email.is_primary == True).
                values(is_primary=False)
            )
            await self.sql.execute(command) 

        command = (
            insert(Email).
            values(
                address=address,
                is_primary=primary,
                is_verified=verified,
                user_pk=self.owner.id
            )
        )
        await self.sql.execute(command)  


    async def get(self, address: str) -> Optional[Email]:
        query = select(Email).where(Email.user_pk == self.owner.id, Email.address == address)
        result = await self.sql.execute(query) 
        return result.scalars().first()
    
    async def list(self) -> list[Email]:
        query = select(Email).where(Email.user_pk == self.owner.id)
        result = await self.sql.execute(query)
        return result.scalars().all()
 
    async def remove(self, email: Email) -> None:
        command = delete(Email).where(Email.user_pk == self.owner.id, Email.address == email.address)
        await self.sql.execute(command)
        email.pk = None