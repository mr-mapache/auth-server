from typing import Annotated
from pydantic import Field
from pydantic_settings import BaseSettings

class CORSMiddlewareSettings(BaseSettings):
    allow_origins: Annotated[list[str], Field(default=['*'])]
    allow_credentials: Annotated[bool, Field(default=True)]
    allow_methods: Annotated[list[str], Field(default=['*'])]
    allow_headers: Annotated[list[str], Field(default=['*'])]

class MiddlewareSettings(BaseSettings):
    cors: Annotated[CORSMiddlewareSettings, Field(default_factory=CORSMiddlewareSettings)]

class APISettings(BaseSettings):
    root_path: Annotated[str, Field(default='/api')]

class Settings(BaseSettings):
    api: Annotated[APISettings, Field(default_factory=APISettings)]
    middleware: Annotated[MiddlewareSettings, Field(default_factory=MiddlewareSettings)]