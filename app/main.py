import logging
import time
from typing import Any
import uuid

from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, Response, status
from fastapi.exceptions import RequestValidationError, ResponseValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.configure_logging import configure_logging
from app.cache.manager import redis_manager
from app.router import api_router

logger = logging.getLogger(__name__)

configure_logging()

# sentry_sdk.init(dsn=settings.SENTRY_DSN,send_default_pii=True,enable_logs=True)

@asynccontextmanager
async def lifespan(app: FastAPI):
    await redis_manager.connect()
    logger.info("Redis connected")
    yield
    logger.info("Redis disconnected")
    await redis_manager.close()


app = FastAPI(lifespan=lifespan)

app.include_router(router=api_router,prefix="/api/v1")

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def log_requests(request: Request, call_next)->Response|Any:
    request_id = str(uuid.uuid1())
    logger.info(f"Request started | ID: {request_id} | {request.method} {request.url}")

    start_time = time.perf_counter()
    response: Response = await call_next(request)
    process_time = (time.perf_counter() - start_time) * 1000

    logger.info(
        f"Request completed | ID: {request_id} "
        f"Status: {response.status_code} | Time {process_time:.2f}ms"
    )
    return response


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(req: Request, exc: RequestValidationError)->JSONResponse:
    logger.error(f"Validation error: {exc.errors()}")
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": "Validation error", "errors": exc.errors()},
    )


@app.exception_handler(ResponseValidationError)
async def validation_exception_handler2(req: Request, exc: ResponseValidationError)->JSONResponse:
    logger.error(f"Validation error: {exc.errors()}")
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": "Validation error", "errors": exc.errors()},
    )


@app.get("/")
async def main_page()->dict:
    return {"Hi": "Guys"}
