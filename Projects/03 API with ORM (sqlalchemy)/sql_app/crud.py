"""
This module contains the utility functions for CRUD.
"""

from sqlalchemy.orm import Session
from sqlalchemy import func
from . import models, schemas
from .utils import get_password_hash


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 0):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    user.password = get_password_hash(user.password)
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, user: schemas.UserCreate, user_id: int):
    user_query = db.query(models.User).filter(models.User.id == user_id)
    user_query.update(user.dict())
    db.commit()
    updated_user = user_query.first()
    return updated_user


def delete_user(db: Session, user: schemas.User):
    db.delete(user)
    db.commit()


def reset_password(db: Session, user_id: int, new_password: str):
    hashed_new_password = get_password_hash(new_password)
    user_query = db.query(models.User).filter(models.User.id == user_id)
    user_query.update({"password": hashed_new_password})
    db.commit()
    updated_user = user_query.first()
    return updated_user



def create_item(db: Session, item: schemas.ItemCreate, user_id: int):
    db_item = models.Item(**item.model_dump(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


# def get_items(db: Session, skip: int = 0, limit: int = 5):
#     return db.query(models.Item).offset(skip).limit(limit).all()

def get_items(db: Session, search: str = "",  skip: int = 0, limit: int = 5):
    return (
        db.query(models.Item, func.count(models.Vote.item_id).label("votes"))
        .join(models.Vote, models.Vote.item_id == models.Item.id, isouter=True)
        .group_by(models.Item.id)
        .filter(models.Item.title.contains(search))
        .offset(skip)
        .limit(limit)
        .all()
    )

# def get_item(db: Session, item_id: int):
#     return db.query(models.Item).filter(models.Item.id == item_id).first()

def get_item(db: Session, item_id: int):
    return (
        db.query(models.Item, func.count(models.Vote.item_id).label("votes"))
        .join(models.Vote, models.Vote.item_id == models.Item.id, isouter=True)
        .group_by(models.Item.id)
        .filter(models.Item.id == item_id)
        .first()
    )


def get_user_items(db: Session, user_id: int):
    return db.query(models.Item).filter(models.Item.owner_id == user_id).all()


def update_item(db: Session, item: schemas.ItemCreate, item_id: int):
    item_query = db.query(models.Item).filter(models.Item.id == item_id)
    item_query.update(item.dict())
    db.commit()
    updated_item = item_query.first()
    return updated_item


def delete_item(db: Session, item: schemas.Item):
    db.delete(item)
    db.commit()
