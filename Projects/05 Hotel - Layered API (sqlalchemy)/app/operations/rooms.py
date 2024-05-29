from fastapi import HTTPException
from sqlalchemy.orm import Session

from ..db.models import DBRoom
from ..operations.schemas import RoomCreateData, RoomUpdateData


def read_all_rooms(session: Session):
    return session.query(DBRoom).all()


def read_room(session: Session, room_id: int):
    db_room = session.get(DBRoom, room_id)
    if db_room is None:
        raise HTTPException(status_code=404, detail="Room not found")
    return db_room


def create_room(session: Session, data: RoomCreateData):
    db_room = DBRoom(**data.model_dump())
    session.add(db_room)
    session.commit()
    session.refresh(db_room)
    return db_room


def update_room(session: Session, room_id: int, data: RoomUpdateData):
    db_room = session.get(DBRoom, room_id)
    if db_room is None:
        raise HTTPException(status_code=404, detail="Room not found")
    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_room, key, value)
    session.commit()
    session.refresh(db_room)
    return db_room


def delete_room(session: Session, room_id: int):
    db_room = session.get(DBRoom, room_id)
    if db_room is None:
        raise HTTPException(status_code=404, detail="Room not found")
    session.delete(db_room)
    session.commit()
