# data/database.py
import sqlite3
from contextlib import contextmanager
from .psv_loader import load_psv


DB_NAME = "app.db"

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()



def initialize_db():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # tạo bảng
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS creatures (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            habitat TEXT,
            power INTEGER
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS explorers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            rank TEXT,
            mission TEXT
        );
    """)

    # load dữ liệu
    creatures = load_psv("creatures.psv")
    explorers = load_psv("explorers.psv")

    for c in creatures:
        cursor.execute(
            "INSERT INTO creatures (name, habitat, power) VALUES (?, ?, ?)",
            (c["name"], c.get("habitat"), c.get("power"))
        )

    for e in explorers:
        cursor.execute(
            "INSERT INTO explorers (name, rank, mission) VALUES (?, ?, ?)",
            (e["name"], e.get("rank"), e.get("mission"))
        )

    conn.commit()
    conn.close()
