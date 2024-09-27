from typing import Annotated

from fastapi import APIRouter, Query

from app.crud.users import (
    delete_user,
    get_user,
    get_user_courses,
    get_users,
)
from app.db.db_setup import SessionDep
from app.dependencies import CurrentUserDep
from app.schemas.courses import Course
from app.schemas.users import User
from app.utils import is_admin_or_current_user

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", response_model=list[User])
async def api_get_users(
    session: SessionDep,
    skip: Annotated[int, Query(ge=0, le=50)] = 0,
    limit: Annotated[int, Query(ge=0, le=20)] = 10,
):
    return await get_users(session, skip=skip, limit=limit)


@router.get("/{user_id}", response_model=User)
async def api_get_user(user_id: int, session: SessionDep):
    return await get_user(session=session, user_id=user_id)


@router.delete("/{user_id}", status_code=204)
async def api_delete_user(
    user_id: int, current_user: CurrentUserDep, session: SessionDep
):
    is_admin_or_current_user(user_id, current_user)
    return await delete_user(session, user_id)


@router.get("/{user_id}/courses", response_model=list[Course])
async def api_get_user_courses(user_id: int, session: SessionDep):
    return await get_user_courses(session, user_id)
