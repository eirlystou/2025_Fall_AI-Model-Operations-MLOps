# main.py
from fastapi import FastAPI
from data.database import initialize_db
from routers import creature, explorer

app = FastAPI(
    title="MVC FastAPI + PSV + SQLite",
    version="1.0"
)

# Khởi tạo DB
initialize_db()

# Đăng ký router
app.include_router(creature.router)
app.include_router(explorer.router)
