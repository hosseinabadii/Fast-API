from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.orm import Session
from .. utils import verify_password
from .. import schemas, crud, oauth2
from ..database import get_db


router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


# @router.get("/", response_model=list[schemas.User])
# def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     users = crud.get_users(db, skip=skip, limit=limit)
#     return users


@router.post("/", response_model=schemas.User, status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(
            status_code=400, detail=f"Email: {user.email} already registered."
        )
    db_user = crud.create_user(db, user)
    return db_user


@router.get("/", response_model=schemas.User)
def read_user(
    current_user: schemas.User = Depends(oauth2.get_current_user),
    db: Session = Depends(get_db),
):
    db_user = crud.get_user(db, current_user.id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User does not exists.")
    return db_user


@router.put("/", status_code=status.HTTP_202_ACCEPTED, response_model=schemas.User)
def update_user(
    user: schemas.UserUpdate,
    current_user: schemas.User = Depends(oauth2.get_current_user),
    db: Session = Depends(get_db),
):
    updated_user = crud.update_user(db, user, current_user.id)
    return updated_user


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    current_user: schemas.User = Depends(oauth2.get_current_user),
    db: Session = Depends(get_db),
):
    crud.delete_user(db, current_user)


@router.put(
    "/reset-password", status_code=status.HTTP_202_ACCEPTED, response_model=schemas.User
)
def reset_password(
    user_reset_password: schemas.UserResetPassword,
    current_user: schemas.User = Depends(oauth2.get_current_user),
    db: Session = Depends(get_db),
):
    db_user = crud.get_user(db, current_user.id)
    if not verify_password(user_reset_password.old_password, db_user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Your old password is not correct.",
        )
    if user_reset_password.new_password != user_reset_password.new_password_again:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="New passwords do not match."
        )
    updated_user = crud.reset_password(db, current_user.id, user_reset_password.new_password)
    return updated_user


@router.get("/user-{user_id}/items", response_model=list[schemas.Item])
def read_user_items(
    user_id: int,
    db: Session = Depends(get_db),
):
    return crud.get_user_items(db, user_id)
