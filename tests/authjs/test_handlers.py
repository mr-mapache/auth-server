from pytest import mark
from pytest import raises
from pytest import fixture
from uuid import UUID
from datetime import datetime, timezone, timedelta
from auth.domain.aggregate import Repository
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


from auth.services.authjs.handlers import (
    handle_create_user,
    handle_update_user,
    handle_delete_user,
    handle_link_account,
    handle_unlink_account,
    handle_create_session,
    handle_update_session,
    handle_delete_session
)

@mark.asyncio
async def test_handle_create_user(repository: Repository):
    command = CreateUser.model_validate({
        'id': '123e4567-e89b-12d3-a456-426614174002',
        'name': 'Test Test',
        'email': 'test@test.com',
        'emailVerified': '2021-01-01T00:00:00Z',
        'image': None
    })
    await handle_create_user(command, repository)
    user = await repository.read(by='id', id='123e4567-e89b-12d3-a456-426614174002')
    assert user.id == UUID('123e4567-e89b-12d3-a456-426614174002')
    assert user.name == 'Test Test'
    user = await repository.read(by='email', address='test@test.com')
    assert user is not None
    assert user.id == UUID('123e4567-e89b-12d3-a456-426614174002')
    emails = await user.emails.list()
    assert emails[0].address == 'test@test.com'
    assert emails[0].is_primary == True
    assert emails[0].is_verified == True
    assert emails[0].verified_at == datetime(2021, 1, 1, 0, 0, 0, tzinfo=timezone.utc)

    with raises(Exception):
        command = CreateUser.model_validate({
            'id': '123e4567-e89b-12d3-a456-426614174003',
            'name': 'Test Test',
            'email': 'test@test.com',
            'emailVerified': '2021-01-01T00:00:00Z',
            'image': None
        })
        await handle_create_user(command, repository)



@mark.asyncio
async def test_handle_update_user(repository: Repository):
    command = CreateUser.model_validate({
        'id': '123e4567-e89b-12d3-a456-426614174002',
        'name': 'Test Test',
        'email': 'test@test.com',
        'emailVerified': None,
        'image': None
    })
    await handle_create_user(command, repository)

    command = UpdateUser.model_validate({
        'id': '123e4567-e89b-12d3-a456-426614174002',
        'name': 'Test Test 2',
        'email': 'other@test.com',
        'emailVerified': '2021-01-01T00:00:00Z',
        'image': None
    })
    await handle_update_user(command, repository)

    user = await repository.read(by='id', id='123e4567-e89b-12d3-a456-426614174002')
    assert user.name == 'Test Test 2'
    emails = await user.emails.list()
    primary = next(email for email in emails if email.is_primary)
    assert primary.address == 'other@test.com'
    assert primary.is_verified == True
    assert primary.verified_at == datetime(2021, 1, 1, 0, 0, 0, tzinfo=timezone.utc)

    await handle_delete_user(DeleteUser.model_validate({
        'id': '123e4567-e89b-12d3-a456-426614174002'
    }), repository )

    with raises(Exception):
        command = UpdateUser.model_validate({
            'id': '123e4567-e89b-12d3-a456-426614174002',
            'name': 'Test Test 2',
            'email': 'other@test.com',
            'emailVerified': '2021-01-01T00:00:00Z',
            'image': None
        })
        await handle_update_user(command, repository)




@mark.asyncio
async def test_handle_accounts(repository: Repository):
    command = CreateUser.model_validate({
        'id': '123e4567-e89b-12d3-a456-426614174002',
        'name': 'Test Test',
        'email': 'test@test.com',
        'emailVerified': None,
        'image': None
    })
    await handle_create_user(command, repository)

    command = LinkAccount.model_validate({
        'userId': '123e4567-e89b-12d3-a456-426614174002',
        'providerAccountId': '123e4567-e89b-12d3-a456-426614174002',
        'provider': 'google',
        'type': 'oauth',
        'access_token': '123456789',
        'token_type': 'Bearer'
    })
    await handle_link_account(command, repository)

    user = await repository.read(by='id', id='123e4567-e89b-12d3-a456-426614174002')
    accounts = await user.accounts.list()
    assert len(accounts) == 1

    command = UnlinkAccount.model_validate({
        'providerAccountId': '123e4567-e89b-12d3-a456-426614174002',
        'provider': 'google',
    })

    await handle_unlink_account(command, repository)

    accounts = await user.accounts.list()
    assert len(accounts) == 0



@mark.asyncio
async def test_sessions(repository: Repository):
    command = CreateUser.model_validate({
        'id': '123e4567-e89b-12d3-a456-426614174002',
        'name': 'Test Test',
        'email': 'test@test.com',
        'emailVerified': '2026-01-01T00:00:00Z',
        'image': None
    })

    await handle_create_user(command, repository)

    command = CreateSession.model_validate({
        'userId': '123e4567-e89b-12d3-a456-426614174002',
        'sessionToken': '123e4567-e89b-12d3-a456-426614174003',
        'expires': '2026-01-01T00:00:00Z'
    })

    await handle_create_session(command, repository)

    user = await repository.read(by='id', id='123e4567-e89b-12d3-a456-426614174002')
    sessions = await user.sessions.list()
    session = sessions[0]
    
    assert session.expires_at - datetime(2026, 1, 1, 0, 0, 0, tzinfo=timezone.utc) < timedelta(seconds=1)

    command = UpdateSession.model_validate({
        'sessionToken': '123e4567-e89b-12d3-a456-426614174003',
        'expires': '2026-01-01T00:00:00Z'
    })

    await handle_update_session(command, repository)
    sessions = await user.sessions.list()
    assert len(sessions) == 1
    session = sessions[0]
    assert session.expires_at - datetime(2027, 1, 1, 0, 0, 0, tzinfo=timezone.utc) < timedelta(seconds=1)

    command = DeleteSession.model_validate({
        'sessionToken': '123e4567-e89b-12d3-a456-426614174003'
    })

    await handle_delete_session(command, repository)
    sessions = await user.sessions.list()
    assert len(sessions) == 0