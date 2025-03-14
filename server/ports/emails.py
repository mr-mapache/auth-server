from abc import ABC, abstractmethod
from typing import Optional
from typing import Protocol
from datetime import datetime

class Email(Protocol):
    
    @property
    def address(self) -> str:
        ...

    @property
    def is_primary(self) -> bool:
        ...

    @property
    def is_verified(self) -> bool:
        ...

# TODO:
#    @property
#    def verified_at(self) -> datetime:
#        ...


class Emails(Protocol):
     
    async def add(self, address: str, primary: bool, verified: bool):...
 
    async def get(self, address: str) -> Optional[Email]:...
 
    async def list(self) -> list[Email]:...
 
    async def remove(self, email: Email) -> None:...