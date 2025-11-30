# backend/schemas.py
from datetime import datetime
from pydantic import BaseModel


# ---------- Book ----------
class BookBase(BaseModel):
    title: str
    author: str
    total_copies: int = 1


class BookCreate(BookBase):
    pass


class BookUpdate(BaseModel):
    title: str | None = None
    author: str | None = None
    total_copies: int | None = None


class BookOut(BookBase):
    id: int
    available_copies: int

    class Config:
        orm_mode = True


# ---------- Loan ----------
class LoanCreate(BaseModel):
    book_id: int
    borrower_name: str


class LoanOut(BaseModel):
    id: int
    book_id: int
    borrower_name: str
    borrow_date: datetime
    return_date: datetime | None
    is_returned: bool

    class Config:
        from_attributes = True
