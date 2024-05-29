"""
This module contains the utility functions for CRUD.
"""

from sqlalchemy.orm import Session
from sqlalchemy.sql import func

from . import models, schemas
from .utils import get_password_hash


###---------------------------------------------------------
### User crud function
###---------------------------------------------------------
def get_user_by_id(session: Session, user_id: int):
    return session.get(models.User, user_id)


def get_user_by_email(session: Session, email: str) -> models.User:
    return session.query(models.User).filter(models.User.email == email).first()


def get_users(session: Session, skip: int = 0, limit: int = 0):
    return session.query(models.User).offset(skip).limit(limit).all()


def create_user(session: Session, user: schemas.UserCreate):
    user.password = get_password_hash(user.password)
    db_user = models.User(**user.model_dump())
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


def update_user(session: Session, user: schemas.UserUpdate, db_user: schemas.User):
    update_data = user.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_user, key, value)
    session.commit()
    session.refresh(db_user)
    return db_user


def delete_user(session: Session, user: schemas.User):
    session.delete(user)
    session.commit()


def reset_password(session: Session, current_user: schemas.User, new_password: str):
    hashed_new_password = get_password_hash(new_password)
    setattr(current_user, "password", hashed_new_password)
    session.commit()


###---------------------------------------------------------
### Item crud function
###---------------------------------------------------------
def get_item_by_id(session: Session, item_id: int):
    return session.get(models.Item, item_id)


def create_item(session: Session, item: schemas.ItemCreate, user_id: int):
    db_item = models.Item(**item.model_dump(), owner_id=user_id)
    session.add(db_item)
    session.commit()
    session.refresh(db_item)
    return db_item


def get_items(
    session: Session,
    skip: int = 0,
    limit: int = 5,
) -> list[schemas.ItemWithVoteCount]:
    items_with_votes = (
        session.query(models.Item, func.count(models.Vote.item_id).label("vote_count"))
        .outerjoin(models.Vote, models.Item.id == models.Vote.item_id)
        .group_by(models.Item.id)
        .offset(skip)
        .limit(limit)
        .all()
    )
    return [
        schemas.ItemWithVoteCount(
            id=item.id,
            title=item.title,
            description=item.description,
            is_public=item.is_public,
            owner_id=item.owner_id,
            vote_count=vote_count,
        )
        for item, vote_count in items_with_votes
    ]


def get_item(session: Session, item_id: int):
    item_with_vote_count = (
        session.query(models.Item, func.count(models.Vote.item_id).label("vote_count"))
        .join(models.Vote, models.Vote.item_id == models.Item.id, isouter=True)
        .filter(models.Item.id == item_id)
        .group_by(models.Item.id)
        .first()
    )
    if item_with_vote_count:
        item: models.Item
        item, vote_count = item_with_vote_count
        item_data = {
            "id": item.id,
            "title": item.title,
            "description": item.description,
            "is_public": item.is_public,
            "owner_id": item.owner_id,
            "vote_count": vote_count,
        }
        return schemas.ItemWithVoteCount(**item_data)
    return None


def get_user_items(session: Session, user_id: int):
    return session.query(models.Item).filter(models.Item.owner_id == user_id).all()


def update_item(session: Session, item: schemas.ItemUpdate, db_item: schemas.Item):
    update_data = item.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_item, key, value)
    session.commit()
    session.refresh(db_item)
    return db_item


def delete_item(session: Session, item: schemas.Item):
    session.delete(item)
    session.commit()
