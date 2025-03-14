from typing import Annotated

from fastapi import APIRouter
from fastapi import Depends 
from fastapi import Form
from fastapi import HTTPException, status 
from fastapi import Request
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from server.schemas import Credentials  