from db.models import Item as DBItem
from db.models import Vote as DBVote
from schemas.item import Item, ItemCreate, ItemUpdate, ItemWithVoteCount
from sqlalchemy.orm import Session
from sqlalchemy.sql import func


def get_item_by_id(session: Session, item_id: int):
    return session.get(DBItem, item_id)


def create_item(session: Session, item: ItemCreate, user_id: int):
    db_item = DBItem(**item.model_dump(), owner_id=user_id)
    session.add(db_item)
    session.commit()
    session.refresh(db_item)
    return db_item


def get_items(
    session: Session,
    skip: int = 0,
    limit: int = 5,
) -> list[ItemWithVoteCount]:
    items_with_votes = (
        session.query(DBItem, func.count(DBVote.item_id).label("vote_count"))
        .outerjoin(DBVote, DBItem.id == DBVote.item_id)
        .group_by(DBItem.id)
        .offset(skip)
        .limit(limit)
        .all()
    )
    return [
        ItemWithVoteCount(
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
        session.query(DBItem, func.count(DBVote.item_id).label("vote_count"))
        .join(DBVote, DBVote.item_id == DBItem.id, isouter=True)
        .filter(DBItem.id == item_id)
        .group_by(DBItem.id)
        .first()
    )
    if item_with_vote_count:
        item: DBItem
        item, vote_count = item_with_vote_count
        item_data = {
            "id": item.id,
            "title": item.title,
            "description": item.description,
            "is_public": item.is_public,
            "owner_id": item.owner_id,
            "vote_count": vote_count,
        }
        return ItemWithVoteCount(**item_data)
    return None


def get_user_items(session: Session, user_id: int):
    return session.query(DBItem).filter(DBItem.owner_id == user_id).all()


def update_item(session: Session, item: ItemUpdate, db_item: Item):
    update_data = item.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_item, key, value)
    session.commit()
    session.refresh(db_item)
    return db_item


def delete_item(session: Session, item: Item):
    session.delete(item)
    session.commit()
