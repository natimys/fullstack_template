import uvicorn
from core.exceptions import AppException, UserAlreadyExists
from core.modules import register_modules
from core.security import jwt_security
from core.settings import get_settings
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer
from loguru import logger
from rich.logging import RichHandler

settings = get_settings()
logger.remove()

logger.add(
    RichHandler(markup=True, rich_tracebacks=True),
    format="{message}",
    level="INFO",
)
logger.add("logs/app.log", rotation="10 MB", level="INFO")
app = FastAPI(swagger_ui_init_oauth={})
bearer_scheme = HTTPBearer()

jwt_security.handle_errors(app)

register_modules(app)


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
    allow_methods=settings.CORS_ALLOW_METHODS,
)


@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})


@app.get("/")
async def root():
    return {"message": "ok"}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
