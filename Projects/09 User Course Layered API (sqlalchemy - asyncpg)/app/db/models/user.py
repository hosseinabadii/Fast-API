from enum import StrEnum, auto
from typing import TYPE_CHECKING

from config import settings
from passlib.context import CryptContext
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy_utils import EmailType

from ..db_setup import Base
from .mixins import Timestamp

if TYPE_CHECKING:
    from .course import CompletedContentBlock, StudentCourse

pwd_context = CryptContext(schemes=[settings.password_schemes], deprecated="auto")


class RoleEnum(StrEnum):
    STUDENT = auto()
    TEACHER = auto()


class User(Timestamp, Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    email: Mapped[str] = mapped_column(
        EmailType, unique=True, index=True, nullable=False
    )
    password: Mapped[str]
    role: Mapped[RoleEnum] = mapped_column(default=RoleEnum.STUDENT)
    is_active: Mapped[bool] = mapped_column(default=False)
    is_admin: Mapped[bool] = mapped_column(default=False)

    student_courses: Mapped[list["StudentCourse"]] = relationship(
        back_populates="student",
    )
    student_content_blocks: Mapped[list["CompletedContentBlock"]] = relationship(
        back_populates="student",
    )

    def set_hashed_password(self, password: str) -> None:
        self.password = pwd_context.hash(password)

    def verify_password(self, plain_password: str) -> bool:
        return pwd_context.verify(plain_password, self.password)

    def activate(self) -> None:
        self.is_active = True

    def deactivate(self) -> None:
        self.is_active = False

    def promote_to_teacher(self) -> None:
        self.role = RoleEnum.TEACHER

    def demote_to_student(self) -> None:
        self.role = RoleEnum.STUDENT

    def __repr__(self) -> str:
        return f"User(email={self.email})"
