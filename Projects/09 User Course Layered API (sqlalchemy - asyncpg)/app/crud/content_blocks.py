from datetime import datetime
from typing import Sequence

from db.models.course import ContentBlock as DBContentBlock
from fastapi import HTTPException
from schemas.content_blocks import ContentBlockCreate, ContentBlockUpdate
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .sections import get_section


async def get_content_block(
    session: AsyncSession, content_block_id: int
) -> DBContentBlock:
    db_content_block = await session.get(DBContentBlock, content_block_id)
    if db_content_block is None:
        raise HTTPException(status_code=404, detail="Content Block not found")
    return db_content_block


async def get_content_blocks(session: AsyncSession) -> Sequence[DBContentBlock]:
    result = await session.execute(select(DBContentBlock))
    return result.scalars().all()


async def create_content_block(
    session: AsyncSession, content_block: ContentBlockCreate
) -> DBContentBlock:
    await get_section(session=session, section_id=content_block.section_id)
    db_content_block = DBContentBlock(**content_block.model_dump(exclude={"url"}))
    db_content_block.url = str(content_block.url)
    session.add(db_content_block)
    await session.commit()
    await session.refresh(db_content_block)
    return db_content_block


async def update_content_block(
    session: AsyncSession, content_block_id: int, content_block: ContentBlockUpdate
) -> DBContentBlock:
    db_content_block = await get_content_block(
        session=session, content_block_id=content_block_id
    )
    updated_data = content_block.model_dump(exclude_unset=True, exclude={"url"})
    for key, value in updated_data.items():
        setattr(db_content_block, key, value)
    db_content_block.url = str(content_block.url)
    db_content_block.updated_at = datetime.now()
    await session.commit()
    await session.refresh(db_content_block)
    return db_content_block


async def delete_content_block(session: AsyncSession, content_block_id: int) -> None:
    db_content_block = await get_content_block(
        session=session, content_block_id=content_block_id
    )
    await session.delete(db_content_block)
    await session.commit()
