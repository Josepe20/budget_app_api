from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
import logging
import time

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        logging.info(f"{request.method} {request.url} completed in {process_time} seconds")
        return response
