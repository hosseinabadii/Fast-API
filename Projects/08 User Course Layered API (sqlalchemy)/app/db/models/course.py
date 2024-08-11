from enum import StrEnum, auto
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy_utils import URLType

from ..db_setup import Base
from .mixins import Timestamp

if TYPE_CHECKING:
    from .user import User


class ContentType(StrEnum):
    LESSON = auto()
    QUIZ = auto()
    ASSIGNMENT = auto()


class Course(Timestamp, Base):
    __tablename__ = "courses"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

    created_by: Mapped["User"] = relationship()
    sections: Mapped[list["Section"]] = relationship(
        back_populates="course",
    )
    student_courses: Mapped[list["StudentCourse"]] = relationship(
        back_populates="course",
    )

    def __repr__(self) -> str:
        return f"Course(title={self.title})"


class StudentCourse(Timestamp, Base):
    """
    Students can be assigned to courses.
    """

    __tablename__ = "student_courses"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    completed: Mapped[bool] = mapped_column(default=False)
    student_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    course_id: Mapped[int] = mapped_column(ForeignKey("courses.id"), nullable=False)

    student: Mapped["User"] = relationship(back_populates="student_courses")
    course: Mapped["Course"] = relationship(back_populates="student_courses")

    def __repr__(self) -> str:
        return f"StudentCourse(student={self.student}, course={self.course})"


class Section(Timestamp, Base):
    __tablename__ = "sections"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    course_id: Mapped[int] = mapped_column(ForeignKey("courses.id"), nullable=False)

    course: Mapped[Course] = relationship(
        back_populates="sections",
    )
    content_blocks: Mapped[list["ContentBlock"]] = relationship(
        back_populates="section"
    )

    def __repr__(self) -> str:
        return f"Section(title={self.title})"


class ContentBlock(Timestamp, Base):
    __tablename__ = "content_blocks"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    type: Mapped["ContentType"]
    url: Mapped[str] = mapped_column(URLType, nullable=True)
    content: Mapped[str] = mapped_column(Text, nullable=True)
    section_id: Mapped[int] = mapped_column(ForeignKey("sections.id"), nullable=False)

    section: Mapped["Section"] = relationship(
        back_populates="content_blocks",
    )
    completed_content_blocks: Mapped[list["CompletedContentBlock"]] = relationship(
        back_populates="content_block"
    )

    def __repr__(self) -> str:
        return f"ContentBlock(title={self.title})"


class CompletedContentBlock(Timestamp, Base):
    """
    This shows when a student has completed a content block.
    """

    __tablename__ = "completed_content_blocks"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    url: Mapped[str] = mapped_column(URLType, nullable=True)
    feedback: Mapped[str] = mapped_column(Text, nullable=True)
    grade: Mapped[int] = mapped_column(default=0)
    student_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    content_block_id: Mapped[int] = mapped_column(
        ForeignKey("content_blocks.id"), nullable=False
    )

    student: Mapped["User"] = relationship(
        back_populates="student_content_blocks",
    )
    content_block: Mapped["ContentBlock"] = relationship(
        back_populates="completed_content_blocks",
    )

    def __repr__(self) -> str:
        return f"CompletedContentBlock(student_id={self.student_id}-content_block={self.content_block_id})"
