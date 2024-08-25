from enum import StrEnum, auto
from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy_utils import EmailType

from ..db_setup import Base
from .mixins import Timestamp

if TYPE_CHECKING:
    from .course import CompletedContentBlock, StudentCourse


class RoleEnum(StrEnum):
    TEACHER = auto()
    STUDENT = auto()


class User(Timestamp, Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    email: Mapped[str] = mapped_column(
        EmailType, unique=True, index=True, nullable=False
    )
    password: Mapped[str]
    role: Mapped[RoleEnum]
    is_active: Mapped[bool] = mapped_column(default=True)
    is_admin: Mapped[bool] = mapped_column(default=False)

    student_courses: Mapped[list["StudentCourse"]] = relationship(
        back_populates="student",
    )
    student_content_blocks: Mapped[list["CompletedContentBlock"]] = relationship(
        back_populates="student",
    )

    def __repr__(self) -> str:
        return f"User(email={self.email})"
