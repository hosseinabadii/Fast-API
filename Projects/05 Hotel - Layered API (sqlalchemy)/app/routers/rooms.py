from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from ..db.database import get_session
from ..operations.rooms import (
    create_room,
    delete_room,
    read_all_rooms,
    read_room,
    update_room,
)
from ..operations.schemas import RoomCreateData, RoomResult, RoomUpdateData

router = APIRouter(tags=["Rooms"])


@router.get("/rooms/", response_model=list[RoomResult])
def api_read_all_rooms(session: Session = Depends(get_session)):
    return read_all_rooms(session)


@router.get("/room/{room_id}", response_model=RoomResult)
def api_read_room(room_id: int, session: Session = Depends(get_session)):
    return read_room(session, room_id)


@router.post("/room/", response_model=RoomResult, status_code=status.HTTP_201_CREATED)
def api_create_room(room: RoomCreateData, session: Session = Depends(get_session)):
    return create_room(session, room)


@router.put(
    "/room/{room_id}", response_model=RoomResult, status_code=status.HTTP_202_ACCEPTED
)
def api_update_room(
    room_id: int, room: RoomUpdateData, session: Session = Depends(get_session)
):
    return update_room(session, room_id, room)


@router.delete("/room/{room_id}", status_code=status.HTTP_204_NO_CONTENT)
def api_delete_room(room_id: int, session: Session = Depends(get_session)):
    return delete_room(session, room_id)
