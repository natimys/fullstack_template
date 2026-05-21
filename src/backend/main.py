import uvicorn
from rich.logging import RichHandler

from core.exceptions import AppException, UserAlreadyExists
from core.modules import register_modules
from core.security import jwt_security
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer
from loguru import logger
from rich.logging import RichHandler

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


@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})


@app.get("/")
async def root():
    return {"message": "ok"}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
