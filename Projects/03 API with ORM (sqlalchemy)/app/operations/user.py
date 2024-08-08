from db.models import User as DBUser
from schemas.user import User, UserCreate, UserUpdate
from sqlalchemy.orm import Session
from utils import get_password_hash


def get_user_by_id(session: Session, user_id: int):
    return session.get(DBUser, user_id)


def get_user_by_email(session: Session, email: str):
    return session.query(DBUser).filter(DBUser.email == email).first()


def get_users(session: Session, skip: int = 0, limit: int = 0):
    return session.query(DBUser).offset(skip).limit(limit).all()


def create_user(session: Session, user: UserCreate):
    user.password = get_password_hash(user.password)
    db_user = DBUser(**user.model_dump())
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


def update_user(session: Session, user: UserUpdate, db_user: User):
    update_data = user.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_user, key, value)
    session.commit()
    session.refresh(db_user)
    return db_user


def delete_user(session: Session, user: User):
    session.delete(user)
    session.commit()


def reset_password(session: Session, current_user: User, new_password: str):
    hashed_new_password = get_password_hash(new_password)
    setattr(current_user, "password", hashed_new_password)
    session.commit()
