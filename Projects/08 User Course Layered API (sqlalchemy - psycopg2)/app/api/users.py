from typing import Annotated

from crud.users import (
    create_user,
    delete_user,
    get_user,
    get_user_by_email,
    get_user_courses,
    get_users,
    update_user,
)
from db.db_setup import SessionDep
from fastapi import APIRouter, HTTPException, Query
from schemas.courses import Course
from schemas.users import User, UserCreate, UserUpdate

router = APIRouter(prefix="/api/users", tags=["Users"])


@router.post("/", response_model=User, status_code=201)
async def api_create_user(user: UserCreate, session: SessionDep):
    db_user = get_user_by_email(session, user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email is already registered")
    return create_user(session, user)


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


@router.put("/{user_id}", response_model=User, status_code=202)
async def api_update_user(user_id: int, user: UserUpdate, session: SessionDep):
    return update_user(session, user_id, user)


@router.delete("/{user_id}", status_code=204)
async def api_delete_user(user_id: int, session: SessionDep):
    return delete_user(session, user_id)


@router.get("/{user_id}/courses", response_model=list[Course])
async def api_get_user_courses(user_id: int, session: SessionDep):
    return get_user_courses(session, user_id)
