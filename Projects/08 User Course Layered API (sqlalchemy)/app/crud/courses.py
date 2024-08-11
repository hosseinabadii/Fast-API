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
    return session.scalars(select(DBCourse)).all()


def create_course(session: Session, course: CourseCreate) -> DBCourse:
    get_user(session=session, user_id=course.user_id)
    db_course = DBCourse(**course.model_dump())
    session.add(db_course)
    session.commit()
    session.refresh(db_course)
    return db_course


def update_course(session: Session, course_id: int, course: CourseUpdate) -> DBCourse:
    db_course = get_course(session=session, course_id=course_id)
    updated_data = course.model_dump(exclude_unset=True)
    for key, value in updated_data.items():
        setattr(db_course, key, value)
    db_course.updated_at = datetime.now()
    session.commit()
    session.refresh(db_course)
    return db_course


def delete_course(session: Session, course_id: int) -> None:
    db_course = get_course(session=session, course_id=course_id)
    session.delete(db_course)
    session.commit()


def get_user_courses(session: Session, user_id: int) -> Sequence[DBCourse]:
    get_user(session=session, user_id=user_id)
    courses = session.scalars(
        select(DBCourse).filter(DBCourse.user_id == user_id)
    ).all()
    return courses