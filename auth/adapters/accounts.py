from typing import override
from typing import Optional

from sqlalchemy.sql import insert, select, update, delete

from auth.domain.ports import Accounts as Collection
from auth.adapters.schemas import User, Account
from auth.adapters.setup import UnitOfWork

class Accounts(Collection):
    def __init__(self, uow: UnitOfWork, user: Optional[User] = None):
        self.uow = uow
        self.user = user

    @override
    def create(self, type: str, provider: str, id: str) -> Account:
        assert self.user is not None, 'User is required for account creation'
        return Account(type=type, provider=provider, id=id, user_pk=self.user.pk)
    
    @override
    async def add(self, account: Account) -> None:
        assert self.user is not None, 'User is required for adding an account'
        command = (
            insert(Account).
            values(type=account.type, provider=account.provider, id=account.id, user_pk=account.user_pk).
            returning(Account.pk)
        )
        result = await self.uow.session.execute(command)
        account.pk = result.scalar()

    @override
    async def get(self, provider: str, id: str) -> Optional[Account]:
        query = select(Account).where(Account.provider == provider, Account.id == id)
        result = await self.uow.session.execute(query)
        return result.scalars().first()
    
    @override
    async def remove(self, account: Account) -> None:
        command = delete(Account).where(Account.pk == account.pk)
        await self.uow.session.execute(command)
        account.pk = None
    
    @override
    async def list(self) -> list[Account]:
        assert self.user is not None, 'User is required for account listing'
        query = select(Account).where(Account.user_pk == self.user.pk)
        result = await self.uow.session.execute(query)
        return result.scalars().all()