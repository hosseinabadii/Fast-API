from datetime import date, timedelta

from pydantic import BaseModel


# Customers schemas
class CustomerCreateData(BaseModel):
    first_name: str
    last_name: str
    email_address: str


class CustomerUpdateData(BaseModel):
    first_name: str | None
    last_name: str | None
    email_address: str | None


# Rooms schemas
class RoomCreateData(BaseModel):
    number: str
    size: int
    price: int


class RoomUpdateData(BaseModel):
    number: str | None
    size: int | None
    price: int | None


# Booking schemas
class BookingCreateData(BaseModel):
    room_id: int
    customer_id: int
    from_date: date = date.today()
    to_date: date = date.today() + timedelta(days=2)


class BookingUpdateData(BaseModel):
    room_id: int | None
    customer_id: int | None
    from_date: date | None
    to_date: date | None
