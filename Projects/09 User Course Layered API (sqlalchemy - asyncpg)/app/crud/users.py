from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.course import Course as DBCourse
from app.db.models.user import User as DBUser
from app.errors import UserNotFound
from app.schemas.users import UserCreate, UserUpdate


async def get_user(session: AsyncSession, user_id: int) -> DBUser:
    db_user = await session.get(DBUser, user_id)
    if db_user is None:
        raise UserNotFound()
    return db_user


async def get_user_by_email(session: AsyncSession, email: str) -> DBUser:
    result = await session.execute(select(DBUser).where(DBUser.email == email))
    return result.scalars().first()


async def get_users(
    session: AsyncSession, skip: int = 0, limit: int = 20
) -> Sequence[DBUser]:
    result = await session.execute(
        select(DBUser).where(DBUser.is_admin.is_(False)).offset(skip).limit(limit)
    )
    return result.scalars().all()


async def create_user(session: AsyncSession, user_data: UserCreate) -> DBUser:
    db_user = DBUser(**user_data.model_dump(exclude={"password"}))
    db_user.set_hashed_password(user_data.password)
    session.add(db_user)
    await session.commit()
    await session.refresh(db_user)
    return db_user


async def update_user(session: AsyncSession, user_id: int, user: UserUpdate) -> DBUser:
    db_user = await get_user(session, user_id)
    updated_data = user.model_dump(exclude_unset=True)
    for key, value in updated_data.items():
        setattr(db_user, key, value)
    await session.commit()
    await session.refresh(db_user)
    return db_user


async def delete_user(session: AsyncSession, user_id: int) -> None:
    db_user = await get_user(session, user_id)
    await session.delete(db_user)
    await session.commit()


async def get_user_courses(session: AsyncSession, user_id: int) -> Sequence[DBCourse]:
    await get_user(session, user_id)
    result = await session.execute(select(DBCourse).where(DBCourse.user_id == user_id))
    return result.scalars().all()
