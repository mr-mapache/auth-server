from uuid import uuid4
from pytest import mark
from pydantic import SecretStr
from pydantic import SecretBytes 
from datetime import datetime, UTC, timedelta
from server.ports.users import Users
 
@mark.asyncio
async def test_users(users: Users):
    id = uuid4()
    user = await users.create(id=id)
    user = await users.get(id)
    assert user.id == id
    await users.delete(id)
    assert not await users.get(id)


@mark.asyncio
async def test_credentials(users: Users):
    id = uuid4()
    user = await users.create(id=id)
    await user.credentials.add(SecretStr('test'), SecretBytes('test'))
    assert await user.credentials.verify(SecretStr('test'), SecretBytes('test'))
    await user.credentials.update(SecretStr('test'), SecretBytes('new'))
    assert not await user.credentials.verify(SecretStr('test'), SecretBytes('test'))
    assert await user.credentials.verify(SecretStr('test'), SecretBytes('new'))
    user = await users.read(by='credentials', username=SecretStr('test'))
    assert user.id == id


@mark.asyncio
async def test_sessions(users: Users):
    id = uuid4()
    user = await users.create(id)
    
    
    payload = {"user": "test_user"}
    expires_in = timedelta(hours=1)
    
    session = await user.sessions.create(expires_in, payload)
    assert session.payload == payload

    session = await user.sessions.get(session.id)
    assert session.payload == payload
    
    session = await user.sessions.create(expires_in, payload)
    assert session.payload == payload

    session_list = await user.sessions.list()
    assert len(session_list) == 2

    await user.sessions.delete(session.id)
    
    session_list = await user.sessions.list()
    assert len(session_list) == 1

    await user.sessions.clear()
    
    session_list = await user.sessions.list()
    assert len(session_list) == 0


@mark.asyncio
async def test_emails(users: Users):
    id = uuid4()
    user = await users.create(id)
    
    await user.emails.add('test@test.com', primary=True, verified=False)
    user = await users.read(by='email', address='test@test.com')
    assert user
    email = await user.emails.get('test@test.com')
    assert email.is_primary == True
    assert email.is_verified == False

    list = await user.emails.list()
    assert len(list) == 1

    
    await user.emails.add('test2@test.com', primary=True, verified=False)

    email = await user.emails.get('test2@test.com')
    assert email.is_primary == True
    assert email.is_verified == False

    
    email = await user.emails.get('tes2t@test.com')
    assert not email


    email = await user.emails.get('test@test.com')
    assert email.is_primary == False
    assert email.is_verified == False
    
    for email in await user.emails.list(): 
        await user.emails.remove(email)

    list = await user.emails.list()
    assert len(list) == 0
