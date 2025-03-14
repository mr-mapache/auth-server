from uuid import UUID
from typing import Any
from typing import Optional
from datetime import datetime
from datetime import timedelta

class Session:
    """
    Represents a session in the server, maintaining user state and expiration.
    A session is a server-side representation of a user's interaction state. The session maintains relevant 
    metadata and payload necessary for continued authentication and request validation.
    """
    
    @property
    def id(self) -> str:
        """
        The session ID is used to uniquely identify an active session instance.
        It is generated upon session creation and should be included in authenticated requests.
        """


    @property
    def payload(self) -> dict[str, Any]:
        """
        A dictionary with data that the session can carry. 
        """

        
    @property
    def expires_at(self) -> datetime:
        """
        This timestamp dictates when the session is no longer valid and should be checked 
        before processing any authenticated requests.
        """

    @property
    def is_expired(self) -> bool:
        """
        A property that dictates if the session is no longer valid (current time > expires_at).
        """

        
class Sessions: 
 
    async def create(self, expires_in: timedelta, payload: dict[str, Any] | None = None) -> Session:
        ... 

    async def get(self, id: str) -> Optional[Session]:         
        ...

    async def delete(self, id: str):
        ...

    async def list(self) -> list[Session]:
        ...

    async def clear(self):
        ...