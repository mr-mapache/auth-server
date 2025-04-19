from json import dumps, loads
from urllib.parse import quote, unquote
from starlette.requests import Request 
from starlette.responses import RedirectResponse
from authlib.integrations.starlette_client import OAuth

class Service:
    ...    

class Authentication(Service):
    def __init__(self, oauth: OAuth):
        self.oauth = oauth

    async def redirect(self, request: Request, provider: str, state: str):
        redirect = request.url_for('callback', provider=provider)
        if provider == 'google':
           return await self.oauth.google.authorize_redirect(request, redirect, state=quote(dumps({'client_redirect_url': state})))

    async def callback(self, request: Request, provider: str):     
        request.session['session'] = ['12345']
        if provider == 'google':
            token = await self.oauth.google.authorize_access_token(request)     
            print(token)
        state = loads(unquote(request.query_params["state"]))
        return RedirectResponse(url=state['client_redirect_url'])