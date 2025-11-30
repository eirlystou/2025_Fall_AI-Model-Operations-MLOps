# backend/main.py
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from . import models, schemas
from .database import engine, Base, get_db

# Tạo bảng
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Library Rental System")


# ---------- BOOK CRUD ----------
@app.post("/books", response_model=schemas.BookOut)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):#Dữ liệu trả về theo cấu trúc được định nghĩa trong schemas.BookOut
    db_book = models.Book(
        title=book.title,
        author=book.author,
        total_copies=book.total_copies,
        available_copies=book.total_copies,
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


@app.get("/books", response_model=List[schemas.BookOut])
def read_books(db: Session = Depends(get_db)):
    return db.query(models.Book).all()


@app.get("/books/{book_id}", response_model=schemas.BookOut)
def read_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(models.Book).get(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@app.put("/books/{book_id}", response_model=schemas.BookOut)
def update_book(
    book_id: int,
    book_update: schemas.BookUpdate,
    db: Session = Depends(get_db),
):
    book = db.query(models.Book).get(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    if book_update.title is not None:
        book.title = book_update.title
    if book_update.author is not None:
        book.author = book_update.author
    if book_update.total_copies is not None:
        # điều chỉnh available khi total thay đổi
        diff = book_update.total_copies - book.total_copies
        book.total_copies = book_update.total_copies
        book.available_copies += diff
        if book.available_copies < 0:
            book.available_copies = 0

    db.commit()
    db.refresh(book)
    return book


@app.delete("/books/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db)):
    # 1. Tìm sách
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="책을 찾을 수 없습니다.")  # Không tìm thấy sách

    # 2. Kiểm tra xem sách có từng được mượn chưa
    has_loan = db.query(models.Loan).filter(models.Loan.book_id == book_id).first()
    if has_loan:
        raise HTTPException(
            status_code=400,
            detail="이미 대여 기록이 있어서 삭제할 수 없습니다."  # Đã có lịch sử mượn nên không xóa
        )

    # 3. Xóa sách
    db.delete(book)
    db.commit()
    return {"message": "도서를 삭제했습니다."}


# ---------- LOAN: borrow / return ----------
@app.post("/loans/borrow", response_model=schemas.LoanOut)
def borrow_book(loan: schemas.LoanCreate, db: Session = Depends(get_db)):
    book = db.query(models.Book).get(loan.book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    if book.available_copies <= 0:
        raise HTTPException(status_code=400, detail="No available copies")

    db_loan = models.Loan(
        book_id=loan.book_id,
        borrower_name=loan.borrower_name,
    )
    book.available_copies -= 1

    db.add(db_loan)
    db.commit()
    db.refresh(db_loan)
    return db_loan


@app.post("/loans/{loan_id}/return", response_model=schemas.LoanOut)
def return_book(loan_id: int, db: Session = Depends(get_db)):
    loan = db.query(models.Loan).get(loan_id)
    if not loan:
        raise HTTPException(status_code=404, detail="Loan not found")
    if loan.is_returned:
        raise HTTPException(status_code=400, detail="Already returned")

    loan.is_returned = True
    from datetime import datetime

    loan.return_date = datetime.utcnow()

    # tăng lại số lượng sách
    book = db.query(models.Book).get(loan.book_id)
    if book:
        book.available_copies += 1

    db.commit()
    db.refresh(loan)
    return loan


@app.get("/loans", response_model=List[schemas.LoanOut])
def read_loans(only_active: bool = False, db: Session = Depends(get_db)):
    q = db.query(models.Loan)
    if only_active:
        q = q.filter(models.Loan.is_returned == False)
    return q.all()
