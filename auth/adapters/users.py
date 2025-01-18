from uuid import UUID, uuid4
from typing import override
from typing import Optional
from dataclasses import dataclass
from sqlalchemy.sql import insert, select, update, delete

from auth.domain.users import Users as Repository
from auth.adapters.schemas import users, emails, accounts
from auth.adapters.utils import UnitOfWork
from auth.adapters.emails import Emails
from auth.adapters.accounts import Accounts
from auth.adapters.sessions import Sessions

@dataclass
class User:
    id: UUID
    name: Optional[str]
    emails: Emails
    accounts: Accounts
    sessions: Sessions
    pk: int = None

class Users(Repository):
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    @override
    async def create(self, id: UUID = None, name: Optional[str] = None) -> User:
        id = id or uuid4()
        command = insert(users).values(user_id=id, user_name=name).returning(users.columns.pk)
        result = await self.uow.sql.execute(command)
        user_pk = result.scalar()
        return User(pk=user_pk, 
            id=id, 
            name=name, 
            emails=Emails(self.uow, user_pk),
            accounts=Accounts(self.uow, user_pk),
            sessions=Sessions(self.uow, id)
        )
    
    @override
    async def read(self, by: str, **kwargs) -> Optional[User]:
        match by:
            case 'id':
                query = select(users).where(users.columns.user_id == kwargs['id'])
                result = await self.uow.sql.execute(query)
                row = result.fetchone()
                return User(
                    pk=row.pk, 
                    id=row.user_id,
                    name=row.user_name, 
                    emails=Emails(self.uow, row.pk),
                    accounts=Accounts(self.uow, row.pk),
                    sessions=Sessions(self.uow, row.user_id)
                ) if row else None
            
            case 'email':
                query = select(users).join(emails).where(emails.columns.email_address == kwargs['address'])
                result = await self.uow.sql.execute(query)
                row = result.fetchone()
                return User(
                    pk=row.pk, 
                    id=row.user_id,
                    name=row.user_name, 
                    emails=Emails(self.uow, row.pk),
                    accounts=Accounts(self.uow, row.pk),
                    sessions=Sessions(self.uow, row.user_id)
                ) if row else None
            
            case 'account':
                query = select(users).join(accounts).where(
                    accounts.columns.account_provider == kwargs['provider'],
                    accounts.columns.account_id == kwargs['id']
                )
                result = await self.uow.sql.execute(query)
                row = result.fetchone()
                return User(
                    pk=row.pk, 
                    id=row.user_id,
                    name=row.user_name, 
                    emails=Emails(self.uow, row.pk),
                    accounts=Accounts(self.uow, row.pk),
                    sessions=Sessions(self.uow, row.user_id)
                ) if row else None
            
            case 'session':
                async for key in self.uow.redis.scan_iter(match=f'*:{kwargs['id']}', count=1):
                    user_id = bytes(key).decode().split(':')[0]
                    query = select(users).where(users.columns.user_id == user_id)
                    result = await self.uow.sql.execute(query)
                    row = result.fetchone()
                    return User(
                        pk=row.pk, 
                        id=row.user_id,
                        name=row.user_name, 
                        emails=Emails(self.uow, row.pk),
                        accounts=Accounts(self.uow, row.pk),
                        sessions=Sessions(self.uow, row.user_id)
                    ) if row else None
            
                            
    @override
    async def update(self, id: UUID, name: Optional[str] = None) -> User:
        command = update(users).where(users.columns.user_id == id).values(user_name=name).returning(users.columns.pk)
        result = await self.uow.sql.execute(command)
        user_pk = result.scalar()
        return User(
            pk=user_pk, 
            id=id, 
            name=name, 
            emails=Emails(self.uow, user_pk),
            accounts=Accounts(self.uow, user_pk),
            sessions=Sessions(self.uow, id)
        )

    @override
    async def delete(self, id: UUID) -> None:
        command = delete(users).where(users.columns.user_id == id)
        await self.uow.sql.execute(command)