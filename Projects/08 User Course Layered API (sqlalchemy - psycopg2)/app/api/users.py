from typing import Annotated

from crud.users import (
    delete_user,
    get_user,
    get_user_courses,
    get_users,
)
from db.db_setup import SessionDep
from fastapi import APIRouter, Query
from schemas.courses import Course
from schemas.users import User
from security.oauth2 import CurrentUserDep

from .utils import is_admin_or_current_user

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", response_model=list[User])
async def api_get_users(
    session: SessionDep,
    skip: Annotated[int, Query(ge=0, le=50)] = 0,
    limit: Annotated[int, Query(ge=0, le=20)] = 10,
):
    return get_users(session, skip=skip, limit=limit)


@router.get("/{user_id}", response_model=User)
async def api_get_user(user_id: int, session: SessionDep):
    return get_user(session, user_id)


@router.delete("/{user_id}", status_code=204)
async def api_delete_user(
    user_id: int, current_user: CurrentUserDep, session: SessionDep
):
    is_admin_or_current_user(user_id, current_user)
    return delete_user(session, user_id)


@router.get("/{user_id}/courses", response_model=list[Course])
async def api_get_user_courses(user_id: int, session: SessionDep):
    return get_user_courses(session, user_id)
