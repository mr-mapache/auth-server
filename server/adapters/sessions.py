from uuid import uuid4
from typing import Optional
from typing import Any
from typing import override
from datetime import datetime, timedelta, UTC
from json import dumps, loads
from dataclasses import dataclass
from redis.asyncio import Redis
from server.settings import Settings
from server.adapters.schemas import Owner
from server.connections import Connections

@dataclass
class Session:
    id: str
    payload: dict[str, Any]
    expires_at: datetime

    @property
    def is_expired(self) -> bool:
        return self.expires_at < datetime.now(tz=UTC)
    
    @property
    def expires_in(self) -> int:
        return int((self.expires_at - datetime.now(tz=UTC)).total_seconds())
    

class Sessions:
    def __init__(self, connections: Connections, settings: Settings, owner: Owner | None):
        self.connections = connections
        self.owner = owner

    @property
    def redis(self) -> Redis:
        return self.connections.cache.redis
 
    async def create(self, expires_in: timedelta, payload: dict[str, Any] | None = None) -> Session:
        assert self.owner is not None, 'User is create a session'
        id=uuid4().hex 
        expires_at = datetime.now(tz=UTC) + expires_in
        await self.redis.set(f'{str(self.owner.id)}:{id}', id, ex=expires_in)
        await self.redis.hset('session', f'{str(self.owner.id)}:{str(id)}', dumps(payload))
        return Session(id=id, payload=payload if payload else {}, expires_at=expires_at)
 

    async def get(self, id: str) -> Optional[Session]:         
        async for key in self.redis.scan_iter(match=f'*:{id}', count=1):
            payload = await self.redis.hget('session', key)
            expires_in = await self.redis.ttl(key)
            expires_at = datetime.now(tz=UTC) + timedelta(seconds=expires_in)
            return Session(id=id, payload=loads(payload) if payload else {}, expires_at=expires_at) if expires_in > 0 else None

    async def delete(self, id: str):
        async for key in self.redis.scan_iter(match=f'*:{id}', count=1):
            await self.redis.delete(key)

    async def list(self) -> list[Session]:
        assert self.owner is not None, 'User is required to list sessions'
        sessions = []
        async for key in self.redis.scan_iter(match=f'{str(self.owner.id)}:*'):
            id = await self.redis.get(key)
            payload = await self.redis.hget('session', key)
            expires_in = await self.redis.ttl(key)
            if expires_in > 0:
                expires_at = datetime.now(tz=UTC) + timedelta(seconds=expires_in)
                sessions.append(Session(id=bytes(id).decode(), payload=loads(payload) if payload else {}, expires_at=expires_at))
        return sessions

    async def clear(self):
        assert self.owner is not None, 'User is required to clear sessions'
        async for key in self.redis.scan_iter(match=f'{str(self.owner.id)}:*'):
            await self.redis.delete(key)