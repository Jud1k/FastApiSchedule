import time
import uuid
import uvicorn
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError, ResponseValidationError
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.student_routes import router as student_router
from app.api.routes.teacher_routes import router as teacher_router
from app.api.routes.subject_routes import router as subject_router
from app.api.routes.room_routes import router as room_router
from app.api.routes.group_routes import router as group_router
from app.api.routes.schedule_routes import router as schedule_router
from app.api.routes.user_routes import router as user_router
from app.logging import configure_logging
from app.redis.manager import redis_manager

logger = logging.getLogger(__name__)

configure_logging()


@asynccontextmanager
async def lifespan(app: FastAPI):
    await redis_manager.connect()
    logger.info("Redis connected")
    yield
    logger.info("Redis disconnected")
    await redis_manager.close()


app = FastAPI(lifespan=lifespan)

app.include_router(student_router, prefix="/api/v1")
app.include_router(teacher_router, prefix="/api/v1")
app.include_router(subject_router, prefix="/api/v1")
app.include_router(room_router, prefix="/api/v1")
app.include_router(group_router, prefix="/api/v1")
app.include_router(schedule_router, prefix="/api/v1")
app.include_router(user_router, prefix="/api/v1")

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
async def log_requests(request: Request, call_next):
    request_id = str(uuid.uuid1())
    logger.info(f"Request started | ID: {request_id} | {request.method} {request.url}")

    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = (time.perf_counter() - start_time) * 1000

    logger.info(
        f"Request completed | ID: {request_id} "
        f"Status: {response.status_code} | Time {process_time:.2f}ms"
    )
    return response


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(req: Request, exc: RequestValidationError):
    logger.error(f"Validation error: {exc.errors()}")
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": "Validation error", "errors": exc.errors()},
    )


@app.exception_handler(ResponseValidationError)
async def validation_exception_handler2(req: Request, exc: ResponseValidationError):
    logger.error(f"Validation error: {exc.errors()}")
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": "Validation error", "errors": exc.errors()},
    )


@app.get("/")
async def main_page():
    return {"Hi": "Guys"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
