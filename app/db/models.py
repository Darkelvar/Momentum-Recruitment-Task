from datetime import datetime
from typing import Optional

from sqlalchemy import Boolean, DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.session import Base


class Book(Base):
    __tablename__ = "books"

    serial_number: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    author: Mapped[str] = mapped_column(String, nullable=False)
    is_borrowed: Mapped[bool] = mapped_column(Boolean, default=False)
    borrowed_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    borrowed_by: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
