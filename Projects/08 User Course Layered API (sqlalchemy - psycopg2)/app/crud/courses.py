from datetime import datetime
from typing import Sequence

from db.models.course import Course as DBCourse
from fastapi import HTTPException
from schemas.courses import CourseCreate, CourseUpdate
from sqlalchemy import select
from sqlalchemy.orm import Session

from .users import get_user


def get_course(session: Session, course_id: int) -> DBCourse:
    db_course = session.get(DBCourse, course_id)
    if db_course is None:
        raise HTTPException(status_code=404, detail="Course not found")
    return db_course


def get_courses(session: Session) -> Sequence[DBCourse]:
    result = session.execute(select(DBCourse))
    return result.scalars().all()


def create_course(session: Session, course: CourseCreate) -> DBCourse:
    get_user(session, course.user_id)
    db_course = DBCourse(**course.model_dump())
    session.add(db_course)
    session.commit()
    session.refresh(db_course)
    return db_course


def update_course(
    session: Session, db_course: DBCourse, course: CourseUpdate
) -> DBCourse:
    updated_data = course.model_dump(exclude_unset=True)
    for key, value in updated_data.items():
        setattr(db_course, key, value)
    db_course.updated_at = datetime.now()
    session.commit()
    session.refresh(db_course)
    return db_course


def delete_course(session: Session, db_course: DBCourse) -> None:
    session.delete(db_course)
    session.commit()
