from typing import Annotated
from fastapi import APIRouter
from fastapi import Request 
from fastapi import Query
from fastapi import Path
from fastapi import status
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

static = StaticFiles(directory='server/static')  
templates = Jinja2Templates('server/templates')

router = APIRouter() 

@router.get('/')
async def get_index(request: Request):
    session = request.session.get('session')
    if not session:
        sign_in_url = request.url_for('get_sign_in_form').include_query_params(state='/')
        return RedirectResponse(url=sign_in_url, status_code=status.HTTP_302_FOUND)
    return session

@router.get('/sign-in')
async def get_sign_in_form(request: Request, state: Annotated[str, Query(...)]): 
    return templates.TemplateResponse(name='sign-in.html', context={'request': request, 'state': state})

@router.post('/sign-in/{provider}')
async def send_sign_in_form(request: Request, provider: Annotated[str, Path(...)], state: Annotated[str, Query(...)]): 
    auth_url = request.url_for('login', provider=provider).include_query_params(state=state) 
    return RedirectResponse(url=auth_url, status_code=status.HTTP_303_SEE_OTHER)