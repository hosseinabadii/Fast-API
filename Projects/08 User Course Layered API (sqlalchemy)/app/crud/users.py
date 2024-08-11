from datetime import datetime
from typing import Sequence

from db.models.user import User as DBUser
from fastapi import HTTPException
from schemas.users import UserCreate, UserUpdate
from sqlalchemy import select
from sqlalchemy.orm import Session


def get_user(session: Session, user_id: int) -> DBUser:
    # db_user = session.query(DBUser).get(user_id)  # 1.x style
    db_user = session.get(DBUser, user_id)  # 2.0 style
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


def get_user_by_email(session: Session, email: str) -> DBUser:
    # return session.query(DBUser).filter(DBUser.email == email).first()  # 1.x style
    # return session.execute(select(DBUser).where(DBUser.email == email)).scalars().first()  # 2.0 style
    return session.scalars(select(DBUser).where(DBUser.email == email)).first()


def get_users(session: Session, skip: int = 0, limit: int = 20) -> Sequence[DBUser]:
    # return session.query(DBUser).offset(skip).limit(limit).all()  # 1.x style
    # return session.execute(select(DBUser).offset(skip).limit(limit)).scalars().all()  # 2.0 style
    return session.scalars(select(DBUser).offset(skip).limit(limit)).all()  # 2.0 style


def create_user(session: Session, user: UserCreate) -> DBUser:
    db_user = DBUser(**user.model_dump())
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


def update_user(session: Session, user_id: int, user: UserUpdate) -> DBUser:
    db_user = get_user(session=session, user_id=user_id)
    updated_data = user.model_dump(exclude_unset=True)
    for key, value in updated_data.items():
        setattr(db_user, key, value)
    db_user.updated_at = datetime.now()
    session.commit()
    session.refresh(db_user)
    return db_user


def delete_user(session: Session, user_id: int) -> None:
    db_user = get_user(session=session, user_id=user_id)
    session.delete(db_user)
    session.commit()
