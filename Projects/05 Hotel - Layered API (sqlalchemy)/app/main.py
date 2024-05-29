from fastapi import FastAPI

from .db.database import create_db
from .routers import bookings, customers, index, rooms

create_db()

app = FastAPI()
app.include_router(index.router)
app.include_router(customers.router)
app.include_router(rooms.router)
app.include_router(bookings.router)
