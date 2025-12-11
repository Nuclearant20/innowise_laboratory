from sqlalchemy import Column, Integer, String
from database import Base


class Book(Base):
    # Table name in the database
    __tablename__ = "books"

    # id: integer, primary key
    id = Column(Integer, primary_key=True, index=True)

    # title: string (required)
    title = Column(String, nullable=False)

    # author: string (required)
    author = Column(String, nullable=False)

    # year: integer (optional)
    year = Column(Integer, nullable=True)
