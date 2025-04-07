import uvicorn
import logging
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError, ResponseValidationError
from fastapi.middleware.cors import CORSMiddleware
from pydantic import ValidationError
from app.api.routes.student_routes import router as student_router
from app.api.routes.teacher_routes import router as teacher_router
from app.api.routes.subject_routes import router as subject_router
from app.api.routes.room_routes import router as room_router
from app.api.routes.group_routes import router as group_router
from app.api.routes.schedule_routes import router as schedule_router

logger = logging.getLogger(__name__)

app = FastAPI()

app.include_router(student_router)
app.include_router(teacher_router)
app.include_router(subject_router)
app.include_router(room_router)
app.include_router(group_router)
app.include_router(schedule_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(req: Request, exc: RequestValidationError):
    logger.error(f"Validation error: {exc.errors()}")
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": "Validation error", "errors": exc.errors()},
    )


@app.exception_handler(ResponseValidationError)
async def validation_exception_handler(req: Request, exc: ResponseValidationError):
    logger.error(f"Validation error: {exc.errors()}")
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": "Validation error", "errors": exc.errors()},
    )


@app.get("/")
async def main_page():
    return {"Hi": "Guys"}


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
