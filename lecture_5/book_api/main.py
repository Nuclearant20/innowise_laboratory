from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from database import get_db, engine
from models import Base
import models
import schemas

# Create database tables
Base.metadata.create_all(bind=engine)

# Create FastAPI app
app = FastAPI(
    title="Book Collection API",
    description="API for managing book collection",
    version="1.0.0"
)

# ========== CREATE BOOK ==========


@app.post("/books/", response_model=schemas.BookResponse)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    db_book = models.Book(
        title=book.title,
        author=book.author,
        year=book.year
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

# ========== GET ALL BOOKS ==========


@app.get("/books/", response_model=List[schemas.BookResponse])
def get_all_books(db: Session = Depends(get_db)):
    books = db.query(models.Book).all()
    return books

# ========== SEARCH BOOKS ==========


@app.get("/books/search/", response_model=List[schemas.BookResponse])
def search_books(
    title: Optional[str] = Query(None),
    author: Optional[str] = Query(None),
    year: Optional[int] = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(models.Book)
    if title:
        query = query.filter(models.Book.title.contains(title))
    if author:
        query = query.filter(models.Book.author.contains(author))
    if year:
        query = query.filter(models.Book.year == year)
    return query.all()

# ========== UPDATE BOOK ==========


@app.put("/books/{book_id}", response_model=schemas.BookResponse)
def update_book(
    book_id: int,
    book_update: schemas.BookUpdate,
    db: Session = Depends(get_db)
):
    db_book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not db_book:
        raise HTTPException(404, f"Book {book_id} not found")

    update_data = book_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_book, field, value)

    db.commit()
    db.refresh(db_book)
    return db_book

# ========== DELETE BOOK ==========


@app.delete("/books/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db)):
    db_book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not db_book:
        raise HTTPException(404, f"Book {book_id} not found")

    db.delete(db_book)
    db.commit()
    return {"message": f"Book {book_id} deleted"}
