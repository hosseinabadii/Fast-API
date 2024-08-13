from datetime import datetime
from typing import Sequence

from db.models.course import Course as DBCourse
from db.models.user import User as DBUser
from fastapi import HTTPException
from schemas.users import UserCreate, UserUpdate
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


async def get_user(session: AsyncSession, user_id: int) -> DBUser:
    db_user = await session.get(DBUser, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


async def get_user_by_email(session: AsyncSession, email: str) -> DBUser:
    result = await session.execute(select(DBUser).where(DBUser.email == email))
    return result.scalars().first()


async def get_users(
    session: AsyncSession, skip: int = 0, limit: int = 20
) -> Sequence[DBUser]:
    result = await session.execute(select(DBUser).offset(skip).limit(limit))
    return result.scalars().all()


async def create_user(session: AsyncSession, user: UserCreate) -> DBUser:
    db_user = DBUser(**user.model_dump())
    session.add(db_user)
    await session.commit()
    await session.refresh(db_user)
    return db_user


async def update_user(session: AsyncSession, user_id: int, user: UserUpdate) -> DBUser:
    db_user = await get_user(session=session, user_id=user_id)
    updated_data = user.model_dump(exclude_unset=True)
    for key, value in updated_data.items():
        setattr(db_user, key, value)
    db_user.updated_at = datetime.now()
    await session.commit()
    await session.refresh(db_user)
    return db_user


async def delete_user(session: AsyncSession, user_id: int) -> None:
    db_user = await get_user(session=session, user_id=user_id)
    await session.delete(db_user)
    await session.commit()


async def get_user_courses(session: AsyncSession, user_id: int) -> Sequence[DBCourse]:
    await get_user(session=session, user_id=user_id)
    result = await session.execute(select(DBCourse).where(DBCourse.user_id == user_id))
    return result.scalars().all()
