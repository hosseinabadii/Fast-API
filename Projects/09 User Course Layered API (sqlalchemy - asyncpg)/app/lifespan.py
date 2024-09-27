from contextlib import asynccontextmanager

from fastapi import FastAPI
from loguru import logger

from app.db.db_setup import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Running lifespan before the application startup!")
    await init_db()
    yield
    logger.info("Running lifespan after the application shutdown!")
