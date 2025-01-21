from fastapi import FastAPI
from auth.controllers.settings import Settings

settings = Settings()

api = FastAPI(root_path=settings.api.root_path)