from fastapi import HTTPException
from sqlalchemy.orm import Session

from ..db.models import DBBooking
from ..operations.customers import read_customer
from ..operations.rooms import read_room
from ..operations.schemas import BookingCreateData, BookingUpdateData


def date_validation(from_date, to_date) -> int:
    days = (to_date - from_date).days
    if days <= 0:
        raise HTTPException(status_code=422, detail="Invalid dates")
    return days


def read_all_bookings(session: Session):
    return session.query(DBBooking).all()


def read_booking(session: Session, booking_id: int):
    db_booking = session.get(DBBooking, booking_id)
    if db_booking is None:
        raise HTTPException(status_code=404, detail="Booking not found")
    return db_booking


def create_booking(session: Session, data: BookingCreateData):
    read_customer(session, data.customer_id)
    room = read_room(session, data.room_id)
    days = date_validation(data.from_date, data.to_date)
    price = room.price * days
    db_booking = DBBooking(**data.model_dump(), price=price)
    session.add(db_booking)
    session.commit()
    session.refresh(db_booking)
    return db_booking


def update_booking(session: Session, booking_id: int, data: BookingUpdateData):
    db_booking = read_booking(session, booking_id)
    room = db_booking.room
    if (data.room_id is not None) and (data.room_id != db_booking.room_id):
        room = read_room(session, data.room_id)

    from_date = data.from_date
    if from_date is None:
        from_date = db_booking.from_date

    to_date = data.to_date
    if to_date is None:
        to_date = db_booking.to_date

    days = date_validation(from_date, to_date)
    price = room.price * days
    update_data = data.model_dump(exclude_unset=True)
    update_data.update(price=price)
    for key, value in update_data.items():
        setattr(db_booking, key, value)
    session.commit()
    session.refresh(db_booking)
    return db_booking


def delete_booking(session: Session, booking_id: int):
    db_booking = session.get(DBBooking, booking_id)
    if db_booking is None:
        raise HTTPException(status_code=404, detail="Booking not found")
    session.delete(db_booking)
    session.commit()
