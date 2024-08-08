from contextlib import asynccontextmanager

from db.database import create_db
from fastapi import FastAPI
from loguru import logger
from routers import bookings, customers, index, rooms


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Running lifespan before the application startup!")
    create_db()
    yield
    logger.info("Running lifespan after the application shutdown!")


app = FastAPI(lifespan=lifespan)
app.include_router(index.router)
app.include_router(customers.router)
app.include_router(rooms.router)
app.include_router(bookings.router)
