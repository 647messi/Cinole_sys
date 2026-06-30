from fastapi import FastAPI

from app.core.logging import setup_logging, get_logger
from app.middleware.request_log import RequestLogMiddleware
from app import router as api_router


setup_logging()
logger = get_logger(__name__)

app = FastAPI(
    title="Enterprise Management API",
    version="0.1.0",
)

app.add_middleware(RequestLogMiddleware)

app.include_router(api_router, prefix="/api")


@app.on_event("startup")
async def startup_event():
    logger.info("FastAPI application started")


@app.get("/")
def root():
    return {"message": "FastAPI server is running"}