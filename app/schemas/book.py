from datetime import datetime, timezone
from typing import Annotated

from pydantic import BaseModel, StringConstraints, field_validator, model_validator
from typing_extensions import Self

SixDigitId = Annotated[
    str, StringConstraints(min_length=6, max_length=6, pattern=r"^\d{6}$")
]


class BookBase(BaseModel):
    serial_number: SixDigitId
    title: str
    author: str

    @model_validator(mode="after")
    def check_empty(self) -> Self:
        if self.title == "":
            raise ValueError("title cannot be an empty string")
        if self.author == "":
            raise ValueError("author cannot be an empty string")
        return self


class BookCreate(BookBase):
    pass


class BookUpdate(BaseModel):
    is_borrowed: bool
    borrowed_at: datetime | None = None
    borrowed_by: SixDigitId | None = None

    @field_validator("borrowed_at")
    @classmethod
    def timezone_to_utc(cls, v: datetime | None, info) -> datetime | None:
        if v is None:
            return None
        elif v.tzinfo is None:
            return v.replace(tzinfo=timezone.utc)
        return v.astimezone(timezone.utc)

    @model_validator(mode="after")
    def check_borrowed_fields(self) -> Self:
        if self.is_borrowed:
            if not self.borrowed_at:
                raise ValueError(
                    "borrowed_at must be provided when is_borrowed is True"
                )
            if not self.borrowed_by:
                raise ValueError(
                    "borrowed_by must be provided when is_borrowed is True"
                )
        return self


class BookOut(BookBase):
    is_borrowed: bool
    borrowed_at: datetime | None
    borrowed_by: str | None


class Config:
    from_attributes = True
