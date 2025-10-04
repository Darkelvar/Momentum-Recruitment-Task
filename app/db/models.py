from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Boolean, DateTime
from datetime import datetime
from typing import Optional
from app.db.session import Base


class Book(Base):
    __tablename__ = "books"

    serial_number: Mapped[str] = mapped_column(String(6), primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    author: Mapped[str] = mapped_column(String, nullable=False)
    is_borrowed: Mapped[bool] = mapped_column(Boolean, default=False)
    borrowed_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    borrowed_by: Mapped[Optional[str]] = mapped_column(String(6), nullable=True)
