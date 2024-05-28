from fastapi import HTTPException
from sqlalchemy.orm import Session

from hotel.db.models import DBBooking
from hotel.operations.customers import read_customer
from hotel.operations.rooms import read_room
from hotel.operations.schemas import BookingCreateData, BookingUpdateData


def date_validation(from_date, to_date) -> int:
    days = (to_date - from_date).days
    if days <= 0:
        raise HTTPException(status_code=422, detail="Invalid dates")
    return days


def read_all_bookings(db: Session):
    return db.query(DBBooking).all()


def read_booking(db: Session, booking_id: int):
    db_booking = db.query(DBBooking).filter(DBBooking.id == booking_id).first()
    if db_booking is None:
        raise HTTPException(status_code=404, detail="Booking not found")
    return db_booking


def create_booking(db: Session, data: BookingCreateData):
    read_customer(db, data.customer_id)
    room = read_room(db, data.room_id)
    days = date_validation(data.from_date, data.to_date)
    price = room.price * days
    db_booking = DBBooking(**data.dict(), price=price)
    db.add(db_booking)
    db.commit()
    db.refresh(db_booking)
    return db_booking


def update_booking(db: Session, booking_id: int, data: BookingUpdateData):
    db_booking = read_booking(db, booking_id)

    room = db_booking.room
    if (data.room_id is not None) and (data.room_id != db_booking.room_id):
        room = read_room(db, data.room_id)

    if (data.customer_id is not None) and (data.customer_id != db_booking.customer_id):
        read_customer(db, data.customer_id)

    from_date = data.from_date
    if from_date is None:
        from_date = db_booking.from_date

    to_date = data.to_date
    if to_date is None:
        to_date = db_booking.to_date

    days = date_validation(from_date, to_date)
    price = room.price * days
    update_data = data.dict(exclude_unset=True)
    update_data.update(price=price)
    for key, value in update_data.items():
        setattr(db_booking, key, value)
    db.commit()
    db.refresh(db_booking)
    return db_booking


def delete_booking(db: Session, booking_id: int):
    db_booking = db.query(DBBooking).filter(DBBooking.id == booking_id).first()
    if db_booking is None:
        raise HTTPException(status_code=404, detail="Booking not found")
    db.delete(db_booking)
    db.commit()
