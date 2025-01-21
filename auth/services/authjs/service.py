from typing import Annotated

from auth.services.authjs.commands import (
    CreateUser,
    UpdateUser,
    DeleteUser,
    LinkAccount,
    UnlinkAccount,
    CreateSession,
    UpdateSession,
    DeleteSession
)

from auth.services.authjs.queries import (
    GetUserById,
    GetUserByEmail,
    GetUserByAccount,
    GetSession,
    GetSessionAndUser
)

from auth.services.authjs.schemas import (
    User,
    Session,
    SessionAndUser
)

from auth.services.authjs.exceptions import (
    UserAlreadyExists,
    UserNotFound,
    EmailAlreadyExists,
    SessionNotFound,
    AccountNotFound
)

from auth.services.schemas import validator
from auth.services.service import Service
from auth.domain.users import Users
from re import sub

service = Service()
service.generator = lambda name: sub(r'([a-z])([A-Z])', r'\1-\2', name).lower()
service.validator = validator

async def port(*args, **kwargs):
    yield

@service.handler
async def handle_create_user(command: CreateUser, users: Users):
    if await users.read(by='id', id=command.user_id) or await users.read(by='email', address=command.user_email_address):
        raise UserAlreadyExists('User already exists')
    
    user = await users.create(id=command.user_id, name=command.user_name)
    email = user.emails.create(
        address=command.user_email_address, 
        is_primary=True, 
        is_verified=True if command.user_email_verified_at else False,
        verified_at=command.user_email_verified_at
    )
    await user.emails.add(email)


@service.handler
async def handle_update_user(command: UpdateUser, users: Users):
    user = await users.read(by='id', id=command.user_id)
    if not user:
        raise UserNotFound('User not found')
    
    if command.user_name:
        await users.update(id=user.id, name=command.user_name)

    if command.user_email_address:
        other_user = await users.read(by='email', address=command.user_email_address)
        if other_user and other_user.id != command.user_id:
            raise EmailAlreadyExists('Email already taken')
        
        emails = await user.emails.list()
        if command.user_email_address not in [email.address for email in emails]:
            email = user.emails.create(
                address=command.user_email_address, 
                is_primary=True, 
                is_verified=True if command.user_email_verified_at else False,
                verified_at=command.user_email_verified_at
            )
            await user.emails.add(email)
        else:
            email = await user.emails.get(address=command.user_email_address)
            email.is_primary = True
            if command.user_email_verified_at:
                email.is_verified = True
                email.verified_at = command.user_email_verified_at
            await user.emails.update(email)



@service.handler
async def handle_delete_user(command: DeleteUser, users: Users):
    user = await users.read(by='id', id=command.user_id)
    if not user:
        raise UserNotFound('User not found')
    await users.delete(id=command.user_id)



@service.handler
async def handle_link_account(command: LinkAccount, users: Users):
    user = await users.read(by='id', id=command.user_id)
    if not user:
        raise UserNotFound('User not found')
    account = user.accounts.create(command.account_type, command.account_provider, command.account_id)
    await user.accounts.add(account)


@service.handler
async def handle_unlink_account(command: UnlinkAccount, users: Users):
    user = await users.read(by='account', provider=command.account_provider, id=command.account_id)
    if not user:
        raise UserNotFound('User not found')
    account = await user.accounts.get(command.account_provider, command.account_id)
    if not account:
        raise AccountNotFound('Account not found')
    await user.accounts.remove(account)


@service.handler
async def handle_create_session(command: CreateSession, users: Users):
    user = await users.read(by='id', id=command.user_id)
    email = next(email for email in await user.emails.list() if email.is_primary)
    payload = {
        'id': str(user.id),
        'email': email.address,
        'emailVerified': email.verified_at.isoformat() if email.verified_at else None,
        'name': user.name,
        'image': None
    }
    session = user.sessions.create(command.session_id, payload=payload, expires_at=command.expires_at)
    await user.sessions.put(session)

@service.handler
async def handle_update_session(command: UpdateSession, users: Users):
    user = await users.read(by='session', id=command.session_id)
    email = next(email for email in await user.emails.list() if email.is_primary)
    payload = {
        'id': str(user.id),
        'email': email.address,
        'emailVerified': email.verified_at.isoformat() if email.verified_at else None,
        'name': user.name,
        'image': None
    }
    session = user.sessions.create(command.session_id, payload=payload, expires_at=command.expires_at)
    await user.sessions.put(session)


@service.handler
async def handle_delete_session(command: DeleteSession, users: Users):
    user = await users.read(by='session', id=command.session_id)
    if not user:
        raise UserNotFound('User not found')
    session = await user.sessions.get(command.session_id)
    if not session:
        raise AccountNotFound('Session not found')
    await user.sessions.remove(session)


@service.handler
async def handle_get_user_by_id(query: GetUserById, users: Users) -> User:
    user = await users.read(by='id', id=query.user_id)
    if not user:
        raise UserNotFound('User not found')
    email = next(email for email in await user.emails.list() if email.is_primary)
    return User(
        id=user.id,
        name=user.name,
        email_address=email.address,
        email_verified_at=email.verified_at.isoformat() if email.verified_at else None,
        profile_image=None
    )



@service.handler
async def handle_get_user_by_email(query: GetUserByEmail, users: Users) -> User:
    user = await users.read(by='email', address=query.email_address)
    if not user:
        raise UserNotFound('User not found')
    email = next(email for email in await user.emails.list() if email.is_primary)
    return User(
        id=user.id,
        name=user.name,
        email_address=email.address,
        email_verified_at=email.verified_at.isoformat() if email.verified_at else None,
        profile_image=None
    )



@service.handler
async def handle_get_user_by_account(query: GetUserByAccount, users: Users) -> User:
    user = await users.read(by='account', provider=query.account_provider, id=query.account_id)
    if not user:
        raise UserNotFound('User not found')
    email = next(email for email in await user.emails.list() if email.is_primary)
    return User(
        id=user.id,
        name=user.name,
        email_address=email.address,
        email_verified_at=email.verified_at.isoformat() if email.verified_at else None,
        profile_image=None
    )

@service.handler
async def handle_get_session(query: GetSession, users: Users) -> Session: 
    session = await users.sessions.get(query.session_id)
    if not session:
        raise SessionNotFound('Session not found')
    return Session(
        id=session.id,
        expires_at=session.expires_at
    )


@service.handler
async def handle_get_session_and_user(query: GetSessionAndUser, users: Users) -> SessionAndUser:
    user = await users.read(by='session', id=query.session_id)
    if not user:
        raise UserNotFound('User not found')
    session = await user.sessions.get(query.session_id)
    if not session:
        raise SessionNotFound('Session not found')
    return SessionAndUser(
        session=Session(
            id=session.id,
            expires_at=session.expires_at
        ),
        user=User.model_validate(session.payload)
    )