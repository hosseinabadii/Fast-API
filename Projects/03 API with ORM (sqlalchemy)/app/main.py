from fastapi import FastAPI
from .database import engine
from .routers import index, auth, user, item, vote
from . import models


# Create the database file and tables if not exists.
models.Base.metadata.create_all(bind=engine)


app = FastAPI()
app.include_router(index.router)
app.include_router(auth.router)
app.include_router(user.router)
app.include_router(item.router)
app.include_router(vote.router)
