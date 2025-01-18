from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from auth.settings import settings

api = FastAPI()
api.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)
