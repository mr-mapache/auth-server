from uuid import UUID
from typing import Optional
from server.ports.credentials import Credentials
from server.ports.sessions import Sessions
from server.ports.emails import Emails

class User:

    @property
    def id(self) -> UUID:
        """
        A globally unique identifier for an User entity. 

        Returns:
            UUID: The unique ID of the User. 
        """
        
    @property
    def credentials(self) -> Credentials:
        ...
    
    @property
    def sessions(self) -> Sessions:
        ...

    @property
    def emails(self) -> Emails:
        ...


class Users:

    async def create(self, id: UUID) -> Optional[User]:...
     
    async def get(self, id: UUID) -> Optional[User]:...

    async def read(self, by: str, **kwargs) -> Optional[User]:...
    
    async def delete(self, id: UUID) -> Optional[User]:...