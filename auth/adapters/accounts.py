from typing import override
from typing import Optional
from dataclasses import dataclass
from sqlalchemy.sql import insert, select, delete

from auth.adapters.schemas import accounts
from auth.adapters.backend import UnitOfWork
from auth.domain.accounts import Accounts as Collection

@dataclass
class Account:
    id: str
    type: str
    provider: str
    pk: int = None

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
            insert(accounts).
            values(
                user_pk=self.user_pk,
                account_type=account.type,
                account_provider=account.provider,
                account_id=account.id
            ).
            returning(accounts.columns.pk)
        )
        result = await self.uow.sql.execute(command)
        account.pk = result.scalar()

    @override
    async def get(self, provider: str, id: str) -> Optional[Account]:
        query = (
            select(accounts).
            where(
                accounts.columns.account_provider == provider,
                accounts.columns.account_id == id
            )
        )
        result = await self.uow.sql.execute(query)
        row = result.fetchone()
        return Account(id=row.account_id, type=row.account_type, provider=row.account_provider, pk=row.pk) if row else None

    @override
    async def list(self) -> list[Account]:
        assert self.user_pk is not None, "Accounts must be associated with a user"
        query = (
            select(accounts).
            where(accounts.columns.user_pk == self.user_pk)
        )
        result = await self.uow.sql.execute(query)
        return [Account(id=row.account_id, type=row.account_type, provider=row.account_provider, pk=row.pk) for row in result]

    @override
    async def remove(self, account: Account):
        command = (
            delete(accounts).
            where(
                accounts.columns.account_provider == account.provider,
                accounts.columns.account_id == account.id
            )
        )
        await self.uow.sql.execute(command)