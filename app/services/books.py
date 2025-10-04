from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Book
from app.schemas.book import BookCreate, BookUpdate


async def create_book(db: AsyncSession, book_in: BookCreate) -> Book:
    book = Book(**book_in.model_dump())
    db.add(book)
    await db.commit()
    await db.refresh(book)
    return book


async def get_books(db: AsyncSession) -> List[Book]:
    result = await db.execute(select(Book))
    return result.scalars().all()


async def get_book(db: AsyncSession, serial_number: int) -> Book | None:
    return await db.get(Book, serial_number)


async def update_book(
    db: AsyncSession, serial_number: int, book_in: BookUpdate
) -> Book | None:
    book = await db.get(Book, serial_number)
    if not book:
        return None

    update_data = book_in.model_dump(exclude_unset=True)
    if update_data.get("is_borrowed") is False:
        update_data["borrowed_at"] = None
        update_data["borrowed_by"] = None

    for field, value in update_data.items():
        setattr(book, field, value)
    await db.commit()
    await db.refresh(book)
    return book


async def delete_book(db: AsyncSession, serial_number: int) -> bool:
    book = await db.get(Book, serial_number)
    if not book:
        return False
    await db.delete(book)
    await db.commit()
    return True
