from crud.sections import (
    create_section,
    delete_section,
    get_section,
    get_sections,
    update_section,
)
from fastapi import APIRouter
from schemas.content_blocks import ContentBlock
from schemas.sections import Section, SectionCreate, SectionUpdate

from .dependencies.core import SessionDep

router = APIRouter(prefix="/api/sections", tags=["Sections"])


@router.post("/", response_model=Section, status_code=201)
async def api_create_section(section: SectionCreate, session: SessionDep):
    return create_section(session=session, section=section)


@router.get("/", response_model=list[Section])
async def api_get_sections(session: SessionDep):
    return get_sections(session=session)


@router.get("/{section_id}", response_model=Section)
async def api_get_section(section_id: int, session: SessionDep):
    return get_section(session=session, section_id=section_id)


@router.put("/{section_id}", response_model=Section, status_code=202)
async def api_update_section(
    section_id: int, section: SectionUpdate, session: SessionDep
):
    return update_section(session=session, section_id=section_id, section=section)


@router.delete("/{section_id}", status_code=204)
async def api_delete_section(section_id: int, session: SessionDep):
    return delete_section(session=session, section_id=section_id)


@router.get("/{section_id}/content-blocks", response_model=list[ContentBlock])
async def api_get_section_content_blocks(section_id: int, session: SessionDep):
    db_section = get_section(session=session, section_id=section_id)
    return db_section.content_blocks
