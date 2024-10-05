from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse


class ExceptionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            response = await call_next(request)
            return response
        except Exception as exc:
            return JSONResponse(
                status_code=400,
                content={
                    "message": str(exc),
                    "ExceptionType": exc.__class__.__name__
                }
            )
