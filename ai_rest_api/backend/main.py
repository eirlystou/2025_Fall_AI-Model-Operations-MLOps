# app/main.py
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from .database import get_db, init_db
from .google_file_search import search_google_file  # Nhập hàm tìm kiếm từ google_file_search.py
from . import crud, models, database

app = FastAPI()

@app.on_event("startup")
def on_startup():
    init_db()  # Tạo các bảng trong cơ sở dữ liệu

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}
# API tạo item mới
@app.post("/items/", response_model=models.ItemResponse)
def create_item(item: models.ItemCreate, db: Session = Depends(database.get_db)):
    db_item = crud.create_item(db=db, item=item)
    return db_item

# API lấy item theo ID
@app.get("/items/{item_id}", response_model=models.ItemResponse)
def read_item(item_id: int, db: Session = Depends(database.get_db)):
    db_item = crud.read_item(db, item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item

# API tìm kiếm, sử dụng Google Gemini API nếu không tìm thấy trong cơ sở dữ liệu
@app.get("/search/")
def search(query: str, db: Session = Depends(get_db)):
    # Tìm trong cơ sở dữ liệu
    db_item = crud.search_item(db, query)
    
    if db_item:
        return db_item
    else:
        # Nếu không tìm thấy trong DB, sử dụng Google Gemini API để tìm kiếm
        google_results = search_google_file(query)
        return {"google_results": google_results}
