from uuid import UUID
from datetime import datetime
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import DateTime
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped

class Schema(DeclarativeBase):
    pk: Mapped[int] = mapped_column(primary_key=True)

class User(Schema):
    __tablename__ = 'users'
    id: Mapped[UUID] = mapped_column('user_id', unique=True, nullable=False)
    name: Mapped[Optional[str]] = mapped_column('user_name')

class Account(Schema):
    __tablename__ = 'accounts'
    type: Mapped[str] = mapped_column('account_type', nullable=False)
    provider: Mapped[str] = mapped_column('account_provider', nullable=False)
    id: Mapped[str] = mapped_column('account_id', nullable=False)
    user_pk: Mapped[int] = mapped_column('user_pk', ForeignKey('users.pk', ondelete='CASCADE'), nullable=False)

class Email(Schema):
    __tablename__ = 'emails'
    address: Mapped[str] = mapped_column('email_address', unique=True, nullable=False)
    is_primary: Mapped[bool] = mapped_column('email_is_primary', nullable=False)
    is_verified: Mapped[bool] = mapped_column('email_is_verified', nullable=False)
    verified_at: Mapped[Optional[datetime]] = mapped_column('email_verified_at', DateTime(timezone=True))
    user_pk: Mapped[int] = mapped_column('user_pk', ForeignKey('users.pk', ondelete='CASCADE'), nullable=False)

users = User.__table__
accounts = Account.__table__
emails = Email.__table__