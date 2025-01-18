from pydantic import Field
from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv

load_dotenv()

class DatabaseSettings(BaseSettings):
    driver: str = Field(default='postgresql+asyncpg')
    host: str = Field(default='localhost')
    port: int = Field(default=5432)
    user: str = Field(...)
    name: str = Field(...)
    password: SecretStr = Field(...)
    
    model_config = SettingsConfigDict(env_prefix='DATABASE_')

    @property
    def uri(self) -> str:
        return f'{self.driver}://{self.user}:{self.password.get_secret_value()}@{self.host}:{self.port}/{self.name}'

class CacheSettings(BaseSettings):
    host: str = Field(default='localhost')
    port: int = Field(default=6379)

    model_config = SettingsConfigDict(env_prefix='CACHE_')

    @property
    def uri(self) -> str:
        return f'redis://{self.host}:{self.port}/0' 

class Settings(BaseSettings):
    database: DatabaseSettings = Field(default_factory=DatabaseSettings)
    cache: CacheSettings = Field(default_factory=CacheSettings)