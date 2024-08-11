from datetime import datetime
from typing import Sequence

from db.models.course import ContentBlock as DBContentBlock
from fastapi import HTTPException
from schemas.content_blocks import ContentBlockCreate, ContentBlockUpdate
from sqlalchemy import select
from sqlalchemy.orm import Session

from .sections import get_section


def get_content_block(session: Session, content_block_id: int) -> DBContentBlock:
    db_content_block = session.get(DBContentBlock, content_block_id)
    if db_content_block is None:
        raise HTTPException(status_code=404, detail="Content Block not found")
    return db_content_block


def get_content_blocks(session: Session) -> Sequence[DBContentBlock]:
    return session.scalars(select(DBContentBlock)).all()


def create_content_block(
    session: Session, content_block: ContentBlockCreate
) -> DBContentBlock:
    get_section(session=session, section_id=content_block.section_id)
    db_content_block = DBContentBlock(**content_block.model_dump(exclude={"url"}))
    db_content_block.url = str(content_block.url)
    session.add(db_content_block)
    session.commit()
    session.refresh(db_content_block)
    return db_content_block


def update_content_block(
    session: Session, content_block_id: int, content_block: ContentBlockUpdate
) -> DBContentBlock:
    db_content_block = get_content_block(
        session=session, content_block_id=content_block_id
    )
    updated_data = content_block.model_dump(exclude_unset=True, exclude={"url"})
    for key, value in updated_data.items():
        setattr(db_content_block, key, value)
    db_content_block.url = str(content_block.url)
    db_content_block.updated_at = datetime.now()
    session.commit()
    session.refresh(db_content_block)
    return db_content_block


def delete_content_block(session: Session, content_block_id: int) -> None:
    db_content_block = get_content_block(
        session=session, content_block_id=content_block_id
    )
    session.delete(db_content_block)
    session.commit()


# def get_user_courses(session: Session, user_id: int):
#     get_user(session=session, user_id=user_id)
#     courses = session.scalars(
#         select(DBCourse).filter(DBCourse.user_id == user_id)
#     ).all()
#     return courses
