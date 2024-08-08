from contextlib import asynccontextmanager

from db.db_setup import init_db
from fastapi import FastAPI
from loguru import logger
from routers import auth, index, item, user, vote


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Running lifespan before the application startup!")
    init_db()
    yield
    logger.info("Running lifespan after the application shutdown!")


app = FastAPI(lifespan=lifespan)


app.include_router(index.router)
app.include_router(auth.router)
app.include_router(user.router)
app.include_router(item.router)
app.include_router(vote.router)
