from typing import override
from typing import Optional
from dataclasses import dataclass
from sqlalchemy.sql import insert, select, delete

from auth.adapters.schemas import Account
from auth.adapters.backend import UnitOfWork
from auth.domain.accounts import Accounts as Collection

class Accounts(Collection):
    def __init__(self, uow: UnitOfWork, user_pk: Optional[int] = None):
        self.user_pk = user_pk
        self.uow = uow

    @override
    def create(self, type: str, provider: str, id: str) -> Account:
        return Account(id=id, type=type, provider=provider)

    @override
    async def add(self, account: Account):
        assert self.user_pk is not None, "Accounts must be associated with a user"
        command = (
            insert(Account).
            values(
                user_pk=self.user_pk,
                type=account.type,
                provider=account.provider,
                id=account.id
            ).
            returning(Account.pk)
        )
        result = await self.uow.sql.execute(command)
        account.pk = result.scalar()

    @override
    async def get(self, provider: str, id: str) -> Optional[Account]:
        query = (
            select(Account).
            where(
                Account.provider == provider,
                Account.id == id
            )
        )
        result = await self.uow.sql.execute(query)
        account = result.scalars().first()
        if account:
            return account
        else:
            return None

    @override
    async def list(self) -> list[Account]:
        assert self.user_pk is not None, "Accounts must be associated with a user"
        query = (
            select(Account).
            where(Account.user_pk == self.user_pk)
        )
        result = await self.uow.sql.execute(query)
        accounts = result.scalars().all()
        return accounts

    @override
    async def remove(self, account: Account):
        command = (
            delete(Account).
            where(
                Account.provider == account.provider,
                Account.id == account.id
            )
        )
        await self.uow.sql.execute(command)
        account.pk = None