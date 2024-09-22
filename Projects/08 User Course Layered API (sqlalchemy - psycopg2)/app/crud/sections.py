from typing import Sequence

from db.models.course import Section as DBSection
from fastapi import HTTPException
from schemas.sections import SectionCreate, SectionUpdate
from sqlalchemy import select
from sqlalchemy.orm import Session

from .courses import get_course


def get_section(session: Session, section_id: int) -> DBSection:
    db_section = session.get(DBSection, section_id)
    if db_section is None:
        raise HTTPException(status_code=404, detail="Section not found")
    return db_section


def get_sections(session: Session) -> Sequence[DBSection]:
    result = session.execute(select(DBSection))
    return result.scalars().all()


def create_section(session: Session, section: SectionCreate) -> DBSection:
    get_course(session, section.course_id)
    db_section = DBSection(**section.model_dump())
    session.add(db_section)
    session.commit()
    session.refresh(db_section)
    return db_section


def update_section(
    session: Session, section_id: int, section: SectionUpdate
) -> DBSection:
    db_section = get_section(session, section_id)
    updated_data = section.model_dump(exclude_unset=True)
    for key, value in updated_data.items():
        setattr(db_section, key, value)
    session.commit()
    session.refresh(db_section)
    return db_section


def delete_section(session: Session, section_id: int) -> None:
    db_section = get_section(session, section_id)
    session.delete(db_section)
    session.commit()
