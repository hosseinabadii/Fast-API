from contextlib import asynccontextmanager

from fastapi import FastAPI
from loguru import logger

from .db import init_db
from .routers import account, index, items, users


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Running lifespan before the application startup!")
    init_db()
    yield
    logger.info("Running lifespan after the application shutdown!")


app = FastAPI(lifespan=lifespan)
app.include_router(index.router)
app.include_router(account.router)
app.include_router(users.router)
app.include_router(items.router)
