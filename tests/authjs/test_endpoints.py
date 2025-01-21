from httpx import AsyncClient

async def test_client(authjs_client: AsyncClient):
    response = await authjs_client.post('/commands/', json ={
        'type': 'create-user',
        'payload': {
            'id': '123e4567-e89b-12d3-a456-426614174002',
            'name': 'Test Test',
            'email': 'test@test.com',
            'emailVerified': '2026-01-01T00:00:00Z',
            'image': None
        }
    }, headers={'TenantID': 'Test'})
    assert response.status_code == 202

    response = await authjs_client.post('/commands/', json ={
        'type': 'create-session',
        'payload': {
            'sessionToken': '123e4567-e89b-12d3-a456-426614174006',
            'userId': '123e4567-e89b-12d3-a456-426614174002',
            'expires': '2026-01-01T00:00:00Z'
        }
    }, headers={'TenantID': 'Test'})

    assert response.status_code == 202

    response = await authjs_client.post('/commands/', json ={
        'type': 'link-account',
        'payload': {
            'userId': '123e4567-e89b-12d3-a456-426614174002',
            'type': 'oauth',
            'provider': 'google',
            'providerAccountId': '123e4567-e89b-12d3-a456-426614174003',
            'access_token': '1234',
            'token_type': 'bearer',
            'expires': 1234
        }
    }, headers={'TenantID': 'Test'})

    assert response.status_code == 202

    response = await authjs_client.post('/commands/', json ={
        'type': 'update-user',
        'payload': {
            'id': '123e4567-e89b-12d3-a456-426614174002',
            'name': 'Test Test',
            'email': 'test@test.com',
            'emailVerified': '2026-01-01T00:00:00Z',
            'image': None
        }
    }, headers={'TenantID': 'Test'})

    response = await authjs_client.post('/queries/', json ={
        'type': 'get-user-by-id',
        'parameters': {
            'id': '123e4567-e89b-12d3-a456-426614174002'
        }
    }, headers={'TenantID': 'Test'})

    assert response.status_code == 200
    assert response.json() == {
        'id': '123e4567-e89b-12d3-a456-426614174002',
        'name': 'Test Test',
        'email': 'test@test.com',
        'emailVerified': '2026-01-01T00:00:00Z',
        'image': None
    }


    response = await authjs_client.post('/commands/', json ={
        'type': 'update-session',
        'payload': {
            'sessionToken': '123e4567-e89b-12d3-a456-426614174006',
            'userId': '123e4567-e89b-12d3-a456-426614174002',
            'expires': '2026-01-01T00:00:00Z'
        }
    }, headers={'TenantID': 'Test'})

    assert response.status_code == 202


    response = await authjs_client.post('/queries/', json ={
        'type': 'get-session-and-user',
        'parameters': {
            'sessionToken': '123e4567-e89b-12d3-a456-426614174006'
        }
    }, headers={'TenantID': 'Test'})

    assert response.status_code == 200


    assert response.json()['user'] == {
        'id': '123e4567-e89b-12d3-a456-426614174002',
        'name': 'Test Test',
        'email': 'test@test.com',
        'emailVerified': '2026-01-01T00:00:00Z',
        'image': None
    }


    response = await authjs_client.post('/queries/', json ={
        'type': 'get-user-by-email',
        'parameters': {
            'email': 'test@test.com'
        }
    }, headers={'TenantID': 'Test'})

    assert response.status_code == 200

    response = await authjs_client.post('/queries/', json ={
        'type': 'get-user-by-account',
        'parameters': {
            'provider': 'google',
            'providerAccountId': '123e4567-e89b-12d3-a456-426614174003',
        }
    }, headers={'TenantID': 'Test'})

    assert response.status_code == 200