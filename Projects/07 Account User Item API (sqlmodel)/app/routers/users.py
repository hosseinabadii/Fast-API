from typing import Sequence

from db.db_setup import get_session
from db.models import User, UserPublic, UserPublicWithItems
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", response_model=list[UserPublic])
def read_users(
    offset: int = 0,
    limit: int = Query(default=3, le=20),
    session: Session = Depends(get_session),
) -> Sequence[User]:
    users = session.exec(
        select(User).offset(offset).where(User.is_active).limit(limit)
    ).all()
    return users


@router.get("/user-{user_id}", response_model=UserPublicWithItems)
def read_user(user_id: int, session: Session = Depends(get_session)) -> User:
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not user.is_active:
        raise HTTPException(status_code=400, detail="This account in not active!")
    return user
