from fastapi import FastAPI

from app.api import account, admin, content_blocks, courses, index, sections, users
from app.errors import register_exceptions
from app.lifespan import lifespan
from app.middleware import register_middleware

app = FastAPI(
    lifespan=lifespan,
    title="Fast API",
    description="Managing students and courses.",
    version="0.0.1",
)


register_middleware(app)
register_exceptions(app)


app.include_router(index.router)
app.include_router(account.router)
app.include_router(admin.router)
app.include_router(users.router)
app.include_router(courses.router)
app.include_router(sections.router)
app.include_router(content_blocks.router)
