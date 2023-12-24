from fastapi import HTTPException
from sqlalchemy.orm import Session

from hotel.db.models import DBRoom
from hotel.operations.schemas import RoomCreateData, RoomUpdateData


def read_all_rooms(db: Session):
    return db.query(DBRoom).all()


def read_room(db: Session, room_id: int):
    db_room = db.query(DBRoom).filter(DBRoom.id == room_id).first()
    if db_room is None:
        raise HTTPException(status_code=404, detail="Room not found")
    return db_room


def create_room(db: Session, data: RoomCreateData):
    db_room = DBRoom(**data.dict())
    db.add(db_room)
    db.commit()
    db.refresh(db_room)
    return db_room


def update_room(db: Session, room_id: int, data: RoomUpdateData):
    db_room = db.query(DBRoom).filter(DBRoom.id == room_id).first()
    if db_room is None:
        raise HTTPException(status_code=404, detail="Room not found")
    update_data = data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_room, key, value)
    db.commit()
    db.refresh(db_room)
    return db_room


def delete_room(db: Session, room_id: int):
    db_room = db.query(DBRoom).filter(DBRoom.id == room_id).first()
    if db_room is None:
        raise HTTPException(status_code=404, detail="Room not found")
    db.delete(db_room)
    db.commit()
