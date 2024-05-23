from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from hotel.db.database import get_db
from hotel.operations.bookings import (
    create_booking,
    delete_booking,
    read_all_bookings,
    read_booking,
    update_booking,
)
from hotel.operations.schemas import BookingCreateData, BookingResult, BookingUpdateData

router = APIRouter(tags=["Bookings"])


@router.get("/bookings/", response_model=list[BookingResult])
def api_read_all_bookings(db: Session = Depends(get_db)):
    return read_all_bookings(db)


@router.get("/booking/{booking_id}", response_model=BookingResult)
def api_read_booking(booking_id: int, db: Session = Depends(get_db)):
    return read_booking(db, booking_id)


@router.post(
    "/booking/", response_model=BookingResult, status_code=status.HTTP_201_CREATED
)
def api_create_booking(booking: BookingCreateData, db: Session = Depends(get_db)):
    return create_booking(db, booking)


@router.put(
    "/booking/{booking_id}",
    response_model=BookingResult,
    status_code=status.HTTP_202_ACCEPTED,
)
def api_update_booking(
    booking_id: int, booking: BookingUpdateData, db: Session = Depends(get_db)
):
    return update_booking(db, booking_id, booking)


@router.delete("/booking/{booking_id}", status_code=status.HTTP_204_NO_CONTENT)
def api_delete_booking(booking_id: int, db: Session = Depends(get_db)):
    return delete_booking(db, booking_id)
