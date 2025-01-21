from secure import Secure
from starlette.middleware.cors import CORSMiddleware as CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware

class SecureHeadersMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        self.secure_headers = Secure.with_default_headers()

    async def dispatch(self, request, call_next):
        response = await call_next(request)
        return self.secure_headers.set_headers_async(response)