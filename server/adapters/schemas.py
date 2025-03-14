from uuid import UUID
from typing import Optional
from typing import Any
from datetime import datetime
from dataclasses import dataclass
from sqlalchemy import ForeignKey
from sqlalchemy import TIMESTAMP
from sqlalchemy import func 
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped 

from server.ports.credentials import Credentials
from server.ports.sessions import Sessions
from server.ports.emails import Emails

@dataclass
class Owner:
    id: Any

class Schema(DeclarativeBase):
    pk: Mapped[int] = mapped_column(primary_key=True)

class User(Schema):
    __tablename__ = 'users'
    __allow_unmapped__ = True
    id: Mapped[UUID] = mapped_column('user_id', unique=True, nullable=False) 
    credentials: Credentials = None
    sessions: Sessions = None
    emails: Emails

class Username(Schema):
    __tablename__ = 'usernames'
    pk: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    value: Mapped[str] = mapped_column('username', nullable=False, unique=True)
    created_at: Mapped[datetime] = mapped_column('username_created_at', TIMESTAMP(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column('username_updated_at', TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now())
    user_pk: Mapped[int] = mapped_column(ForeignKey('users.pk', ondelete='CASCADE'), nullable=False)

class Password(Schema):
    __tablename__ = 'passwords'
    pk: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    hash: Mapped[bytes] = mapped_column('password_hash', nullable=False)
    version: Mapped[int] = mapped_column('password_version', default=1)
    is_active: Mapped[bool] = mapped_column('password_is_active', default=True)
    created_at: Mapped[datetime] = mapped_column('password_created_at', TIMESTAMP(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column('password_updated_at', TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now())
    username_pk: Mapped[int] = mapped_column(ForeignKey('usernames.pk', ondelete='CASCADE'), nullable=False)
 
class Email(Schema):
    __tablename__ = 'emails'
    address: Mapped[str] = mapped_column('email_address', unique=True, nullable=False)
    is_primary: Mapped[bool] = mapped_column('email_is_primary', nullable=False)
    is_verified: Mapped[bool] = mapped_column('email_is_verified', nullable=False)
    user_pk: Mapped[int] = mapped_column('user_pk', ForeignKey('users.pk', ondelete='CASCADE'), nullable=False)