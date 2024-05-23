from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import crud, oauth2, schemas
from ..database import get_db

router = APIRouter(
    prefix="/items",
    tags=["Items"],
)


@router.get("/", response_model=list[schemas.ItemVote])
def read_items(
    search: str = "", skip: int = 0, limit: int = 5, db: Session = Depends(get_db)
):
    # items = crud.get_items(db, skip=skip, limit=limit)
    items = crud.get_items(db, search, skip, limit)
    return items


@router.get("/{item_id}", response_model=schemas.ItemVote)
def read_item(
    item_id: int,
    db: Session = Depends(get_db),
):
    item = crud.get_item(db, item_id)
    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with id={item_id} does not exist.",
        )
    return item


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Item)
def create_item(
    item: schemas.ItemCreate,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(oauth2.get_current_user),
):
    return crud.create_item(db, item, current_user.id)


@router.put(
    "/{item_id}", status_code=status.HTTP_202_ACCEPTED, response_model=schemas.Item
)
def update_item(
    item_id: int,
    item: schemas.ItemCreate,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    db_item = crud.get_item(db, item_id)
    if db_item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with id={item_id} does not exist.",
        )
    if db_item.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to update this item.",
        )
    updated_item = crud.update_item(db, item, item_id)
    return updated_item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    item = crud.get_item(db, item_id)
    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with id={item_id} does not exist.",
        )
    if item.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to delete this item.",
        )
    crud.delete_item(db, item)
