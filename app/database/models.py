from datetime import date
from uuid import uuid4

from sqlalchemy import CheckConstraint, ForeignKey, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.types import JSON


class Base(DeclarativeBase):
    type_annotation_map = {dict: JSON}


class Librarians(Base):
    __tablename__ = "librarians"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    password: Mapped[str] = mapped_column(nullable=False)


class Readers(Base):
    __tablename__ = "readers"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)

    borrowed_books: Mapped[list["BorrowedBooks"]] = relationship(
        back_populates="reader"
    )


def generate_isbn():
    return uuid4().hex[:13]


class Books(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(nullable=False)
    author: Mapped[str] = mapped_column(nullable=False)
    publication_year: Mapped[int] = mapped_column(nullable=True)
    isbn: Mapped[str] = mapped_column(default=generate_isbn, unique=True)
    copies_quality: Mapped[int] = mapped_column(default=1)

    borrowed: Mapped[list["BorrowedBooks"]] = relationship(
        back_populates="book"
    )

    __table_args__ = (
        CheckConstraint(
            copies_quality >= 0, name="check_quantity_non_negative"
        ),
    )


class BorrowedBooks(Base):
    __tablename__ = "borrow_books"

    id: Mapped[int] = mapped_column(primary_key=True)
    book_id: Mapped[int] = mapped_column(
        ForeignKey("books.id", ondelete="RESTRICT")
    )
    reader_id: Mapped[int] = mapped_column(
        ForeignKey("readers.id", ondelete="RESTRICT")
    )
    borrow_date: Mapped[date] = mapped_column(default=func.current_date())
    return_date: Mapped[date] = mapped_column(default=None)

    book: Mapped["Books"] = relationship(back_populates="borrowed")
    reader: Mapped["Readers"] = relationship(back_populates="borrowed_books")
