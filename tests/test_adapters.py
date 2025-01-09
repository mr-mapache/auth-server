from pytest import mark
from datetime import datetime, timezone, timedelta
from uuid import UUID
from auth.domain.ports import Users
from auth.domain.ports import Accounts
from auth.domain.ports import Emails
from auth.domain.ports import Sessions
from auth.domain.aggregate import Repository

@mark.asyncio
async def test_users(users: Users):
    user = users.create()
    id = user.id
    await users.add(user)
    assert getattr(user, 'pk') is not None
    user = await users.get(id)
    assert user.id == id
    assert user.name == None
    user.name = 'Test'
    await users.update(user)
    user = await users.get(id)
    assert user.name == 'Test'
    await users.remove(user)
    assert await users.get(id) == None

@mark.asyncio
async def test_accounts(accounts: Accounts):
    account = accounts.create('oauth', 'google', '123')
    await accounts.add(account)
    assert getattr(account, 'pk') is not None
    account = await accounts.get('google', '123')
    assert account.provider == 'google'
    assert account.id == '123'
    assert account.type == 'oauth'
    account_list = await accounts.list()
    assert len(account_list) == 1
    await accounts.remove(account)
    assert await accounts.get('google', '123') == None


@mark.asyncio
async def test_emails(emails: Emails):
    email = emails.create('test@test.com', True, False)
    await emails.add(email)
    assert getattr(email, 'pk') is not None
    email = await emails.get('test@test.com')
    assert email.address == 'test@test.com'
    assert email.is_verified == False
    assert email.is_primary == True
    email.address = 'other@test.com'
    email.is_primary = True
    email.is_verified = True
    email.verified_at = datetime.now(timezone.utc)
    await emails.update(email)
    email = await emails.get('other@test.com')
    assert email.address == 'other@test.com'
    assert email.is_verified == True
    assert email.is_primary == True
    email_list = await emails.list()
    assert len(email_list) == 1
    await emails.remove(email)
    assert await emails.get('other@test.com') == None

@mark.asyncio
async def test_sessions(sessions: Sessions):
    session = sessions.create(UUID('00000000-0000-0000-0000-000000000000'), {'test': 'test'}, datetime.now(timezone.utc) + timedelta(seconds=60))
    await sessions.put(session)
    
    session = await sessions.get(UUID('00000000-0000-0000-0000-000000000000'))
    assert session.id == UUID('00000000-0000-0000-0000-000000000000')
    assert session.payload == {'test': 'test'}
    assert session.expires_at > datetime.now(timezone.utc)

    session_list = await sessions.list()
    assert len(session_list) == 1
    await sessions.remove(session)
    assert await sessions.get(UUID('00000000-0000-0000-0000-000000000000')) == None

    session = sessions.create(UUID('00000000-0000-0000-0000-000000000000'), {'test': 'test'}, datetime.now(timezone.utc) - timedelta(seconds=60))
    await sessions.put(session)
    assert await sessions.get(UUID('00000000-0000-0000-0000-000000000000')) == None

    session_list = [
        sessions.create(UUID('00000000-0000-0000-0000-000000000000'), {'test': 'test'}, datetime.now(timezone.utc) + timedelta(seconds=60)),
        sessions.create(UUID('00000000-0000-0000-0000-000000000001'), {'test': 'test'}, datetime.now(timezone.utc) + timedelta(seconds=60)),
        sessions.create(UUID('00000000-0000-0000-0000-000000000002'), {'test': 'test'}, datetime.now(timezone.utc) + timedelta(seconds=60)),
    ]

    for session in session_list:
        await sessions.put(session)

    session_list = await sessions.list()
    assert len(session_list) == 3

    await sessions.clear()
    session_list = await sessions.list()
    assert len(session_list) == 0

@mark.asyncio
async def test_repository(repository: Repository):
    user = await repository.create(name='Test')
    assert user.name == 'Test'