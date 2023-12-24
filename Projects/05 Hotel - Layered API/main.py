from fastapi import FastAPI

from hotel.db.database import create_db
from hotel.routers import bookings, customers, index, rooms

create_db()

app = FastAPI()
app.include_router(index.router)
app.include_router(customers.router)
app.include_router(rooms.router)
app.include_router(bookings.router)
