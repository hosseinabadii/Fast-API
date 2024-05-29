from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import crud, schemas
from ..database import get_session
from ..oauth2 import get_current_user

router = APIRouter(
    prefix="/items",
    tags=["Items"],
)


@router.get("/")
def read_items(
    skip: int = 0,
    limit: int = 5,
    session: Session = Depends(get_session),
):
    items = crud.get_items(session, skip, limit)
    return items


@router.get("/{item_id}", response_model=schemas.ItemWithVoteCount)
def read_item(
    item_id: int,
    session: Session = Depends(get_session),
):
    item_with_votes = crud.get_item(session, item_id)
    if not item_with_votes:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with id={item_id} does not exist.",
        )
    return item_with_votes


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Item)
def create_item(
    item: schemas.ItemCreate,
    session: Session = Depends(get_session),
    current_user: schemas.User = Depends(get_current_user),
):
    return crud.create_item(session, item, current_user.id)


@router.put(
    "/{item_id}", status_code=status.HTTP_202_ACCEPTED, response_model=schemas.Item
)
def update_item(
    item_id: int,
    item: schemas.ItemUpdate,
    session: Session = Depends(get_session),
    current_user: schemas.User = Depends(get_current_user),
):
    db_item = crud.get_item_by_id(session, item_id)
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
    updated_item = crud.update_item(session, item, db_item)
    return updated_item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(
    item_id: int,
    session: Session = Depends(get_session),
    current_user: schemas.User = Depends(get_current_user),
):
    db_item = crud.get_item_by_id(session, item_id)
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
    crud.delete_item(session, db_item)
