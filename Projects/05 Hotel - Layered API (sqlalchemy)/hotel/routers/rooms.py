from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from hotel.db.database import get_db
from hotel.operations.rooms import (
    create_room,
    delete_room,
    read_all_rooms,
    read_room,
    update_room,
)
from hotel.operations.schemas import RoomCreateData, RoomResult, RoomUpdateData

router = APIRouter(tags=["Rooms"])


@router.get("/rooms/", response_model=list[RoomResult])
def api_read_all_rooms(db: Session = Depends(get_db)):
    return read_all_rooms(db)


@router.get("/room/{room_id}", response_model=RoomResult)
def api_read_room(room_id: int, db: Session = Depends(get_db)):
    return read_room(db, room_id)


@router.post("/room/", response_model=RoomResult, status_code=status.HTTP_201_CREATED)
def api_create_room(room: RoomCreateData, db: Session = Depends(get_db)):
    return create_room(db, room)


@router.put(
    "/room/{room_id}", response_model=RoomResult, status_code=status.HTTP_202_ACCEPTED
)
def api_update_room(room_id: int, room: RoomUpdateData, db: Session = Depends(get_db)):
    return update_room(db, room_id, room)


@router.delete("/room/{room_id}", status_code=status.HTTP_204_NO_CONTENT)
def api_delete_room(room_id: int, db: Session = Depends(get_db)):
    return delete_room(db, room_id)
