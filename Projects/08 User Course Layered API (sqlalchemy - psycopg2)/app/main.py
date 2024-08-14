from contextlib import asynccontextmanager

from api import content_blocks, courses, index, sections, users
from db.db_setup import init_db
from fastapi import FastAPI
from loguru import logger
from security import auth_routers


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Running lifespan before the application startup!")
    init_db()
    yield
    logger.info("Running lifespan after the application shutdown!")


app = FastAPI(
    lifespan=lifespan,
    title="Fast API",
    description="Managing students and courses.",
    version="0.0.1",
)

app.include_router(auth_routers.router)
app.include_router(index.router)
app.include_router(users.router)
app.include_router(courses.router)
app.include_router(sections.router)
app.include_router(content_blocks.router)
