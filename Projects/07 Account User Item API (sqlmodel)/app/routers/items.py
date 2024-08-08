from typing import Sequence

from db.db_setup import get_session
from db.models import Item, ItemCreate, ItemPublic, ItemPublicForUser, ItemUpdate, User
from fastapi import APIRouter, Depends, HTTPException, Query, status
from oauth2 import get_current_user
from sqlmodel import Session, select

router = APIRouter(prefix="/items", tags=["Items"])


@router.post("/", response_model=ItemPublic, status_code=status.HTTP_201_CREATED)
def create_item(
    item: ItemCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
) -> Item:
    extra_data = {"user": current_user}
    db_item = Item.model_validate(item, update=extra_data)
    session.add(db_item)
    session.commit()
    session.refresh(db_item)
    return db_item


@router.get("/my-items", response_model=list[ItemPublicForUser])
def read_my_items(
    offset: int = 0,
    limit: int = Query(default=3, le=20),
    current_user: User = Depends(get_current_user),
) -> Sequence[Item]:
    return current_user.items[offset : offset + limit]


@router.get("/my-items/{item_id}", response_model=ItemPublic)
def read_my_item(
    item_id: int,
    current_user: User = Depends(get_current_user),
) -> Item:
    for item in current_user.items:
        if item_id == item.id:
            return item
    raise HTTPException(status_code=404, detail="Item not found or it is not yours.")


@router.get("/", response_model=list[ItemPublic])
def read_items(
    offset: int = 0,
    limit: int = Query(default=3, le=20),
    session: Session = Depends(get_session),
) -> Sequence[Item]:
    items = session.exec(
        select(Item).offset(offset).limit(limit).where(Item.is_public)
    ).all()
    return items


@router.get("/{item_id}", response_model=ItemPublic)
def read_item(item_id: int, session: Session = Depends(get_session)) -> Item:
    db_item = session.get(Item, item_id)
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    if not db_item.is_public:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have access to this item.",
        )
    return db_item


@router.patch(
    "/{item_id}",
    response_model=ItemPublic,
    status_code=status.HTTP_202_ACCEPTED,
)
def update_item(
    item_id: int,
    item: ItemUpdate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
) -> Item:
    db_item = session.get(Item, item_id)
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    if db_item.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to update this user.",
        )
    item_data = item.model_dump(exclude_unset=True)
    db_item.sqlmodel_update(item_data)
    session.add(db_item)
    session.commit()
    session.refresh(db_item)
    return db_item


@router.delete("/{item_id}", response_model=ItemPublic)
def delete_item(
    item_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
) -> Item:
    db_item = session.get(Item, item_id)
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    if db_item.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to update this user.",
        )
    session.delete(db_item)
    session.commit()
    return db_item
