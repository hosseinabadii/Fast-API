from db.db_setup import get_session
from fastapi import APIRouter, Depends, HTTPException, status
from oauth2 import get_current_user
from operations.item import get_user_items
from operations.user import (
    create_user,
    delete_user,
    get_user_by_email,
    get_user_by_id,
    get_users,
    reset_password,
    update_user,
)
from schemas.item import Item
from schemas.user import User, UserCreate, UserResetPassword, UserUpdate
from sqlalchemy.orm import Session
from utils import verify_password

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
def api_create_user(user: UserCreate, session: Session = Depends(get_session)):
    db_user = get_user_by_email(session, email=user.email)
    if db_user:
        raise HTTPException(
            status_code=400, detail=f"Email: {user.email} already registered."
        )
    db_user = create_user(session, user)
    return db_user


@router.get("/", response_model=list[User])
def api_get_users(
    skip: int = 0,
    limit: int = 100,
    session: Session = Depends(get_session),
):
    return get_users(session, skip=skip, limit=limit)


@router.get("/{user_id}", response_model=User)
def api_get_user_by_id(
    user_id: int,
    session: Session = Depends(get_session),
):
    db_user = get_user_by_id(session, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User does not exists.")
    return db_user


@router.put("/", status_code=status.HTTP_202_ACCEPTED, response_model=User)
def api_update_user(
    user: UserUpdate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    db_user = get_user_by_id(session, current_user.id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User does not exists.")
    updated_user = update_user(session, user, db_user)
    return updated_user


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
def api_delete_user(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    delete_user(session, current_user)


@router.put("/reset-password", status_code=status.HTTP_202_ACCEPTED)
def api_reset_password(
    user_reset_password: UserResetPassword,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    if not verify_password(user_reset_password.old_password, current_user.password):  # type: ignore
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Your old password is not correct.",
        )
    if user_reset_password.new_password != user_reset_password.new_password_again:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="New passwords do not match."
        )
    return reset_password(session, current_user, user_reset_password.new_password)


@router.get("/user-{user_id}/items", response_model=list[Item])
def api_get_user_items(
    user_id: int,
    session: Session = Depends(get_session),
):
    return get_user_items(session, user_id)
