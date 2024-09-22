from typing import Sequence

from db.models.course import Course as DBCourse
from fastapi import HTTPException
from schemas.courses import CourseCreate, CourseUpdate
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


async def get_course(session: AsyncSession, course_id: int) -> DBCourse:
    db_course = await session.get(DBCourse, course_id)
    if db_course is None:
        raise HTTPException(status_code=404, detail="Course not found")
    return db_course


async def get_courses(session: AsyncSession) -> Sequence[DBCourse]:
    result = await session.execute(select(DBCourse))
    return result.scalars().all()


async def create_course(
    session: AsyncSession, course: CourseCreate, user_id: int
) -> DBCourse:
    course_data = course.model_dump()
    course_data.update({"user_id": user_id})
    db_course = DBCourse(**course_data)
    session.add(db_course)
    await session.commit()
    await session.refresh(db_course)
    return db_course


async def update_course(
    session: AsyncSession, db_course: DBCourse, course: CourseUpdate
) -> DBCourse:
    updated_data = course.model_dump(exclude_unset=True)
    for key, value in updated_data.items():
        setattr(db_course, key, value)
    await session.commit()
    await session.refresh(db_course)
    return db_course


async def delete_course(session: AsyncSession, db_course: DBCourse) -> None:
    await session.delete(db_course)
    await session.commit()
