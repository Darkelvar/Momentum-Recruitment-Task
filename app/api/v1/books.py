from typing import List

from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_session
from app.schemas.book import BookCreate, BookOut, BookUpdate
from app.services import books

router = APIRouter(prefix="/books", tags=["books"])


@router.post("", response_model=BookOut)
async def create_book(book_in: BookCreate, db: AsyncSession = Depends(get_session)):
    return await books.create_book(db, book_in)


@router.get("", response_model=List[BookOut])
async def list_books(db: AsyncSession = Depends(get_session)):
    return await books.get_books(db)


@router.get("/{serial_number}", response_model=BookOut)
async def get_book(serial_number: str, db: AsyncSession = Depends(get_session)):
    book = await books.get_book(db, serial_number)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@router.put("/{serial_number}", response_model=BookOut)
async def update_book(
    serial_number: str, book_in: BookUpdate, db: AsyncSession = Depends(get_session)
):
    book = await books.update_book(db, serial_number, book_in)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@router.delete("/{serial_number}")
async def delete_book(serial_number: str, db: AsyncSession = Depends(get_session)):
    success = await books.delete_book(db, serial_number)
    if not success:
        raise HTTPException(status_code=404, detail="Book not found")
    return Response(status_code=204)
