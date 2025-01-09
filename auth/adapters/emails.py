from typing import override
from typing import Optional
from datetime import datetime

from sqlalchemy.sql import insert, select, update, delete

from auth.domain.ports import Emails as Collection
from auth.adapters.schemas import User, Email
from auth.adapters.setup import UnitOfWork

class Emails(Collection):
    def __init__(self, uow: UnitOfWork, user: Optional[User] = None):
        self.uow = uow
        self.user = user

    @override
    def create(self, address: str, is_primary: bool, is_verified: bool, verified_at: Optional[datetime] = None) -> Email:
        return Email(address=address, is_primary=is_primary, is_verified=is_verified, verified_at=verified_at)
    
    @override
    async def add(self, email: Email):
        assert self.user is not None, 'User is required for email creation'
        if email.is_primary:
            command = (
                update(Email).
                where(
                    Email.user_pk == self.user.pk,
                    Email.is_primary == True
                ).
                values(is_primary=False)
            )
            await self.uow.session.execute(command)


        command = (
            insert(Email).
            values(
                address=email.address,
                is_primary=email.is_primary,
                is_verified=email.is_verified,
                verified_at=email.verified_at,
                user_pk=self.user.pk).
            returning(Email.pk)
        )
        result = await self.uow.session.execute(command)
        email.pk = result.scalar()


    @override
    async def get(self, address: str) -> Optional[Email]:
        query = select(Email).where(Email.address == address)
        result = await self.uow.session.execute(query)
        return result.scalars().first()
    
    
    @override
    async def update(self, email: Email):
        assert self.user is not None, 'User is required for email update'
        if email.is_primary:
            command = (
                update(Email).
                where(
                    Email.user_pk == self.user.pk,
                    Email.is_primary == True,
                    Email.pk != email.pk
                ).
                values(is_primary=False)
            )
            await self.uow.session.execute(command)

        command = (
            update(Email).
            where(Email.pk == email.pk).
            values(
                address=email.address,
                is_primary=email.is_primary,
                is_verified=email.is_verified,
                verified_at=email.verified_at
            )
        )
        await self.uow.session.execute(command)

    @override
    async def remove(self, email: Email):
        command = delete(Email).where(Email.pk == email.pk)
        await self.uow.session.execute(command)
        email.pk = None

    @override
    async def list(self) -> list[Email]:
        assert self.user is not None, 'User is required for email listing'
        query = select(Email).where(Email.user_pk == self.user.pk)
        result = await self.uow.session.execute(query)
        return result.scalars().all()