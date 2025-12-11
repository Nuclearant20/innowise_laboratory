from pydantic import BaseModel
from typing import Optional

# Schema for creating a book


class BookCreate(BaseModel):
    title: str
    author: str
    year: Optional[int] = None

# Schema for updating a book


class BookUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    year: Optional[int] = None

# Schema for book response


class BookResponse(BaseModel):
    id: int
    title: str
    author: str
    year: Optional[int] = None

    class Config:
        from_attributes = True  # Formerly known as orm_mode
