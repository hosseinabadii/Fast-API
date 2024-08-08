from db.db_setup import get_session
from fastapi import APIRouter, Depends, HTTPException, status
from oauth2 import get_current_user
from operations.item import (
    create_item,
    delete_item,
    get_item,
    get_item_by_id,
    get_items,
    update_item,
)
from schemas.item import Item, ItemCreate, ItemUpdate, ItemWithVoteCount
from schemas.user import User
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/items",
    tags=["Items"],
)


@router.get("/")
def api_get_items(
    skip: int = 0,
    limit: int = 5,
    session: Session = Depends(get_session),
):
    items = get_items(session, skip, limit)
    return items


@router.get("/{item_id}", response_model=ItemWithVoteCount)
def api_get_item(
    item_id: int,
    session: Session = Depends(get_session),
):
    item_with_votes = get_item(session, item_id)
    if not item_with_votes:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with id={item_id} does not exist.",
        )
    return item_with_votes


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Item)
def api_create_item(
    item: ItemCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    return create_item(session, item, current_user.id)


@router.put("/{item_id}", status_code=status.HTTP_202_ACCEPTED, response_model=Item)
def api_update_item(
    item_id: int,
    item: ItemUpdate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    db_item = get_item_by_id(session, item_id)
    if not db_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with id={item_id} does not exist.",
        )
    if db_item.owner is not current_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to update this item.",
        )
    updated_item = update_item(session, item, db_item)
    return updated_item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def api_delete_item(
    item_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    db_item = get_item_by_id(session, item_id)
    if not db_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with id={item_id} does not exist.",
        )
    if db_item.owner is not current_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to delete this item.",
        )
    delete_item(session, db_item)
