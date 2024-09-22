from typing import Sequence

from db.models.course import Section as DBSection
from fastapi import HTTPException
from schemas.sections import SectionCreate, SectionUpdate
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .courses import get_course


async def get_section(session: AsyncSession, section_id: int) -> DBSection:
    db_section = await session.get(DBSection, section_id)
    if db_section is None:
        raise HTTPException(status_code=404, detail="Section not found")
    return db_section


async def get_sections(session: AsyncSession) -> Sequence[DBSection]:
    result = await session.execute(select(DBSection))
    return result.scalars().all()


async def create_section(session: AsyncSession, section: SectionCreate) -> DBSection:
    await get_course(session, section.course_id)
    db_section = DBSection(**section.model_dump())
    session.add(db_section)
    await session.commit()
    await session.refresh(db_section)
    return db_section


async def update_section(
    session: AsyncSession, section_id: int, section: SectionUpdate
) -> DBSection:
    db_section = await get_section(session, section_id)
    updated_data = section.model_dump(exclude_unset=True)
    for key, value in updated_data.items():
        setattr(db_section, key, value)
    await session.commit()
    await session.refresh(db_section)
    return db_section


async def delete_section(session: AsyncSession, section_id: int) -> None:
    db_section = await get_section(session, section_id)
    await session.delete(db_section)
    await session.commit()
