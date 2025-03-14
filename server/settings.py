from datetime import timedelta
from typing import Annotated
from dotenv import load_dotenv
from pydantic import Field
from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()

class PostgreSQLSettings(BaseSettings):
    driver: Annotated[str, Field(default='postgresql+asyncpg')]
    host: Annotated[str, Field(default='localhost')]
    port: Annotated[int, Field(default=5432)]
    user: Annotated[str, Field(...)]
    name: Annotated[str, Field(...)]
    password: Annotated[SecretStr, Field(...)]
    model_config = SettingsConfigDict(env_prefix='POSTGRESQL_')

    @property
    def uri(self) -> str:
        return f'{self.driver}://{self.user}:{self.password.get_secret_value()}@{self.host}:{self.port}/{self.name}'


class RedisSettings(BaseSettings):
    host: Annotated[str, Field(default='localhost')]
    port: Annotated[int, Field(default=6379)]
    model_config = SettingsConfigDict(env_prefix='CACHE_')

    @property
    def uri(self) -> str:
        return f'redis://{self.host}:{self.port}/0' 


class CORSMiddleware(BaseSettings):
    allow_origins: Annotated[list[str], Field(default_factory=lambda: ['*'])]
    allow_credentials: Annotated[bool, Field(default=True)]
    allow_methods: Annotated[list[str], Field(default_factory=lambda: ['*'])]
    allow_headers: Annotated[list[str], Field(default_factory=lambda: ['*'])]

class MiddlewareSettings(BaseSettings):
    cors: Annotated[CORSMiddleware, Field(default_factory=CORSMiddleware)]


class Cryptography(BaseSettings):
    key: Annotated[SecretStr, Field(...)]
    model_config = SettingsConfigDict(env_prefix='CRYPTOGRAPHY_')

class SessionsSettings(BaseSettings):
    ttl: Annotated[int, Field(default=259200)]

class Settings(BaseSettings):
    
    database: Annotated[PostgreSQLSettings, Field(default_factory=PostgreSQLSettings)]
    cache: Annotated[RedisSettings, Field(default_factory=RedisSettings)]
    middleware: Annotated[MiddlewareSettings, Field(default_factory=MiddlewareSettings)] 
    cryptography: Annotated[Cryptography, Field(default_factory=Cryptography)]
    sessions: Annotated[SessionsSettings, Field(default_factory=SessionsSettings)]