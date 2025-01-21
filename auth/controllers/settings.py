from typing import Annotated
from pydantic import Field
from pydantic_settings import BaseSettings

class CORSMiddlewareSettings(BaseSettings):
    allow_origins: Annotated[list[str], Field(default=['*'])]
    allow_credentials: Annotated[bool, Field(default=True)]
    allow_methods: Annotated[list[str], Field(default=['*'])]
    allow_headers: Annotated[list[str], Field(default=['*'])]
    allow_origin_regex: Annotated[str | None, Field(default=None)]
    expose_headers: Annotated[list[str], Field(default=[])]
    max_age: Annotated[int, Field(default=600)]

class MiddlewareSettings(BaseSettings):
    cors: Annotated[CORSMiddlewareSettings, Field(default_factory=CORSMiddlewareSettings)]

class TransportSettings(BaseSettings):
    root_path: Annotated[str, Field(default='/api')]

class Settings(BaseSettings):
    transport: Annotated[TransportSettings, Field(default_factory=TransportSettings)]
    middleware: Annotated[MiddlewareSettings, Field(default_factory=MiddlewareSettings)]