from datetime import datetime
from typing import Sequence

from db.models.course import Course as DBCourse
from fastapi import HTTPException
from schemas.courses import CourseCreate, CourseUpdate
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .users import get_user


async def get_course(session: AsyncSession, course_id: int) -> DBCourse:
    db_course = await session.get(DBCourse, course_id)
    if db_course is None:
        raise HTTPException(status_code=404, detail="Course not found")
    return db_course


async def get_courses(session: AsyncSession) -> Sequence[DBCourse]:
    result = await session.execute(select(DBCourse))
    return result.scalars().all()


async def create_course(session: AsyncSession, course: CourseCreate) -> DBCourse:
    await get_user(session=session, user_id=course.user_id)
    db_course = DBCourse(**course.model_dump())
    session.add(db_course)
    await session.commit()
    await session.refresh(db_course)
    return db_course


async def update_course(
    session: AsyncSession, course_id: int, course: CourseUpdate
) -> DBCourse:
    db_course = await get_course(session=session, course_id=course_id)
    updated_data = course.model_dump(exclude_unset=True)
    for key, value in updated_data.items():
        setattr(db_course, key, value)
    db_course.updated_at = datetime.now()
    await session.commit()
    await session.refresh(db_course)
    return db_course


async def delete_course(session: AsyncSession, course_id: int) -> None:
    db_course = await get_course(session=session, course_id=course_id)
    await session.delete(db_course)
    await session.commit()
