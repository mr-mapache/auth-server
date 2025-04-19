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
    model_config = SettingsConfigDict(env_prefix='REDIS_')

    @property
    def uri(self) -> str:
        return f'redis://{self.host}:{self.port}/0'  


class GoogleSettings(BaseSettings):
    client_id: Annotated[str, Field(...)]
    client_secret: Annotated[SecretStr, Field(...)]
    redirect_uri: Annotated[str, Field('http://localhost:8000/api/auth/google/callback')]
    server_metadata_url: Annotated[str, Field(default='https://accounts.google.com/.well-known/openid-configuration')]
    client_kwargs: Annotated[dict, Field(default={'scope': 'openid profile email'})]
    model_config = SettingsConfigDict(env_prefix='GOOGLE_')


class Cryptography(BaseSettings):
    key: Annotated[SecretStr, Field(...)]
    model_config = SettingsConfigDict(env_prefix='CRYPTOGRAPHY_')
    

class SessionSettings(BaseSettings):
    secret_key: Annotated[SecretStr, Field(...)]
    session_cookie: Annotated[str, Field(default='session')]
    max_age: Annotated[int, Field(default=timedelta(days=14).total_seconds())]
    path: Annotated[str, Field(default='/')]
    same_site: Annotated[str, Field(default='lax')]
    https_only: Annotated[bool, Field(default=False)]
    domain: Annotated[str | None, Field(default=None)]
    model_config = SettingsConfigDict(env_prefix='SESSIONS_')
    

class CORSSettings(BaseSettings):
    allow_origins: Annotated[list[str], Field(default=['http://localhost:3000', 'https://localhost:8000'])]
    allow_credentials: Annotated[bool, Field(default=True)]
    allow_methods: Annotated[list[str], Field(default=['*'])]
    allow_headers: Annotated[list[str], Field(default=['*'])] 
    expose_headers: Annotated[list[str], Field(default=['*'])]
    max_age: Annotated[int, Field(default=600)]
    model_config = SettingsConfigDict(env_prefix='CORS_')


class APISettings(BaseSettings):
    host: Annotated[str, Field(default='localhost')]
    port: Annotated[int, Field(default=8000)]
    model_config = SettingsConfigDict(env_prefix='API_')


class Settings(BaseSettings):
    database: Annotated[PostgreSQLSettings, Field(default_factory=PostgreSQLSettings)]
    cache: Annotated[RedisSettings, Field(default_factory=RedisSettings)] 
    google: Annotated[GoogleSettings, Field(default_factory=GoogleSettings)]
    cryptography: Annotated[Cryptography, Field(default_factory=Cryptography)] 
    sessions: Annotated[SessionSettings, Field(default_factory=SessionSettings)]
    cors: Annotated[CORSSettings, Field(default_factory=CORSSettings)]
    api: Annotated[APISettings, Field(default_factory=APISettings)]