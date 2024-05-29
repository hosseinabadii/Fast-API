from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from ..db.database import get_session
from ..operations.bookings import (
    create_booking,
    delete_booking,
    read_all_bookings,
    read_booking,
    update_booking,
)
from ..operations.schemas import BookingCreateData, BookingResult, BookingUpdateData

router = APIRouter(tags=["Bookings"])


@router.get("/bookings/", response_model=list[BookingResult])
def api_read_all_bookings(session: Session = Depends(get_session)):
    return read_all_bookings(session)


@router.get("/booking/{booking_id}", response_model=BookingResult)
def api_read_booking(booking_id: int, session: Session = Depends(get_session)):
    return read_booking(session, booking_id)


@router.post(
    "/booking/", response_model=BookingResult, status_code=status.HTTP_201_CREATED
)
def api_create_booking(
    booking: BookingCreateData, session: Session = Depends(get_session)
):
    return create_booking(session, booking)


@router.put(
    "/booking/{booking_id}",
    response_model=BookingResult,
    status_code=status.HTTP_202_ACCEPTED,
)
def api_update_booking(
    booking_id: int, booking: BookingUpdateData, session: Session = Depends(get_session)
):
    return update_booking(session, booking_id, booking)


@router.delete("/booking/{booking_id}", status_code=status.HTTP_204_NO_CONTENT)
def api_delete_booking(booking_id: int, session: Session = Depends(get_session)):
    return delete_booking(session, booking_id)
