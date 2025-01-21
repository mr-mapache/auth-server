from pytest import mark
from auth.services import Service

import pytest
from datetime import datetime, timedelta, timezone
from uuid import UUID

@pytest.mark.asyncio
async def test_create_and_get_user(authjs_service: Service):
    # Create a user
    await authjs_service.execute('create-user', {
        'id': '00000000-0000-0000-0000-000000000000',
        'email': 'test@test.com',
        'name': 'Test User',
        'emailVerified': None,
        'image': None
    })

    # Fetch the user by ID
    user = await authjs_service.execute('get-user-by-id', {
        'id': '00000000-0000-0000-0000-000000000000'
    })

    # Assert user details
    assert user.email_address == 'test@test.com'
    assert user.name == 'Test User'
    assert user.email_verified_at is None
    assert user.profile_image is None


@pytest.mark.asyncio
async def test_user_email_verification(authjs_service: Service):
    # Create a user with verified email
    await authjs_service.execute('create-user', {
        'id': '11111111-1111-1111-1111-111111111111',
        'email': 'verified@test.com',
        'name': 'Verified User',
        'emailVerified': '2025-01-01T00:00:00Z',
        'image': None
    })

    # Fetch the user by email
    user = await authjs_service.execute('get-user-by-email', {
        'email': 'verified@test.com'
    })

    # Assert email verification
    assert user.email_verified_at == datetime(2025, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
    assert user.name == 'Verified User'


@pytest.mark.asyncio
async def test_create_and_link_account(authjs_service: Service):
    # Create a user
    await authjs_service.execute('create-user', {
        'id': '22222222-2222-2222-2222-222222222222',
        'email': 'account@test.com',
        'name': 'Account User',
        'emailVerified': None,
        'image': None
    })

    # Link an account
    await authjs_service.execute('link-account', {
        'userId': '22222222-2222-2222-2222-222222222222',
        'providerAccountId': 'account123',
        'provider': 'google',
        'type': 'oauth',
        'access_token': 'access123',
        'token_type': 'Bearer'
    })

    # Fetch the user by account
    user = await authjs_service.execute('get-user-by-account', {
        'provider': 'google',
        'providerAccountId': 'account123'
    })

    # Assert user details
    assert user.id == UUID('22222222-2222-2222-2222-222222222222')
    assert user.email_address == 'account@test.com'
    assert user.name == 'Account User'


@pytest.mark.asyncio
async def test_create_and_manage_session(authjs_service: Service):
    # Create a user
    await authjs_service.execute('create-user', {
        'id': '33333333-3333-3333-3333-333333333333',
        'email': 'session@test.com',
        'name': 'Session User',
        'emailVerified': '2025-01-01T00:00:00Z',
        'image': None
    })

    # Create a session
    await authjs_service.execute('create-session', {
        'userId': '33333333-3333-3333-3333-333333333333',
        'sessionToken': 'session123',
        'expires': '2026-01-01T00:00:00Z'
    })

    # Fetch the session and user
    session_data = await authjs_service.execute('get-session-and-user', {
        'sessionToken': 'session123'
    })

    # Assert session details
    session = session_data.session
    user = session_data.user
    assert user.id == UUID('33333333-3333-3333-3333-333333333333')

    # Update the session
    await authjs_service.execute('update-session', {
        'sessionToken': 'session123',
        'expires': '2027-01-01T00:00:00Z'
    })

    # Verify updated session
    updated_session_data = await authjs_service.execute('get-session-and-user', {
        'sessionToken': 'session123'
    })
    assert updated_session_data.session.id == session.id
    # Delete the session
    await authjs_service.execute('delete-session', {
        'sessionToken': 'session123'
    })

    # Ensure session is deleted
    with pytest.raises(Exception):
        await authjs_service.execute('get-session-and-user', {
            'sessionToken': 'session123'
        })
