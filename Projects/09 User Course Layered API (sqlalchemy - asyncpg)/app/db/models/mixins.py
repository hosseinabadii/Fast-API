from datetime import UTC, datetime

from sqlalchemy import TIMESTAMP
from sqlalchemy.orm import Mapped, declarative_mixin, mapped_column


@declarative_mixin
class Timestamp:
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), default=datetime.now(UTC), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), default=datetime.now(UTC), nullable=False
    )
