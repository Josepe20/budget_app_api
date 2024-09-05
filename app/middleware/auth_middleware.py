from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import HTTPException, Request
from jose import jwt, JWTError
from decouple import config

SECRET_KEY = config('SECRET_KEY')
ALGORITHM = config('ALGORITHM')

class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Skip token validation for public routes
        if request.url.path in ["/users/login", "/users/register"]:
            return await call_next(request)
        
        # Otherwise, perform token validation
        token = request.headers.get('Authorization')
        if token is None:
            raise HTTPException(status_code=401, detail="Authorization token missing")
        
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        except JWTError:
            raise HTTPException(status_code=401, detail="Invalid token")
        
        return await call_next(request)

