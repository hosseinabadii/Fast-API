from datetime import datetime
from typing import Sequence

from db.models.course import Course as DBCourse
from db.models.user import User as DBUser
from fastapi import HTTPException
from schemas.users import UserCreate, UserUpdate
from sqlalchemy import select
from sqlalchemy.orm import Session
from security.utils import get_password_hash

def get_user(session: Session, user_id: int) -> DBUser:
    db_user = session.get(DBUser, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


def get_user_by_email(session: Session, email: str) -> DBUser | None:
    result = session.execute(select(DBUser).where(DBUser.email == email))
    return result.scalars().first()


def get_users(session: Session, skip: int = 0, limit: int = 20) -> Sequence[DBUser]:
    result = session.execute(select(DBUser).offset(skip).limit(limit))
    return result.scalars().all()


def create_user(session: Session, user: UserCreate) -> DBUser:
    db_user = DBUser(**user.model_dump(exclude={"password"}))
    db_user.password = get_password_hash(user.password)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


def update_user(session: Session, user_id: int, user: UserUpdate) -> DBUser:
    db_user = get_user(session, user_id)
    updated_data = user.model_dump(exclude_unset=True)
    for key, value in updated_data.items():
        setattr(db_user, key, value)
    db_user.updated_at = datetime.now()
    session.commit()
    session.refresh(db_user)
    return db_user


def delete_user(session: Session, user_id: int) -> None:
    db_user = get_user(session, user_id)
    session.delete(db_user)
    session.commit()


def get_user_courses(session: Session, user_id: int) -> Sequence[DBCourse]:
    get_user(session, user_id)
    result = session.execute(select(DBCourse).where(DBCourse.user_id == user_id))
    return result.scalars().all()
