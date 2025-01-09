from typing import Optional
from uuid import UUID
from auth.domain.aggregate import User
from auth.domain.aggregate import Repository as Base
from auth.adapters.setup import UnitOfWork
from auth.adapters.users import Users as Roots
from auth.adapters.accounts import Accounts
from auth.adapters.emails import Emails
from auth.adapters.sessions import Sessions

class Repository(Base):
    def __init__(self, uow: UnitOfWork):
        self.uow = uow
        self.roots = Roots(uow)
    
    async def create(self, id: UUID = None, name: Optional[str] = None) -> User:
        root = self.roots.create(id, name)
        await self.roots.add(root)
        return User(root.id, root.name, Emails(self.uow, root), Accounts(self.uow, root), Sessions(self.uow, root))
    
    async def update(self, id: UUID, **kwargs):
        root = await self.roots.get(id)
        if root:
            for key, value in kwargs.items():
                setattr(root, key, value)
            await self.roots.update(root)

    async def read(self, by: str, **kwargs) -> Optional[User]:
        match by:
            case 'id':
                root = await self.roots.get(**kwargs)
            case 'email':
                root = await self.roots.get_by_email(**kwargs)
            case 'account':
                root = await self.roots.get_by_account(**kwargs)
            case 'session':
                root = await self.roots.get_by_session(**kwargs)
            case _:
                root = None
        return User(root.id, root.name, Emails(self.uow, root),Accounts(self.uow, root),Sessions(self.uow, root)) if root else None

    async def delete(self, id: UUID):
        root = await self.roots.get(id)
        if root:
            await self.roots.remove(root)