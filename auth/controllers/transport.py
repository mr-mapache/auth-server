from fastapi import FastAPI
from auth.controllers.settings import Settings
from auth.controllers.middleware import CORSMiddleware

settings = Settings()
transport = FastAPI(root_path=settings.transport.root_path)
transport.add_middleware(
    CORSMiddleware, 
    allow_origins=settings.middleware.cors.allow_origins,
    allow_credentials=settings.middleware.cors.allow_credentials,
    allow_methods=settings.middleware.cors.allow_methods,
    allow_headers=settings.middleware.cors.allow_headers,
    expose_headers=settings.middleware.cors.expose_headers,
    max_age=settings.middleware.cors.max_age
)