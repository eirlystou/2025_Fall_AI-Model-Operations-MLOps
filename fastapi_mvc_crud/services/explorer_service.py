# services/explorer_service.py
from typing import List, Optional
from sqlite3 import Connection
from models.explorer import ExplorerCreate, ExplorerGet


class ExplorerService:

    @staticmethod
    def get_all(conn: Connection) -> List[ExplorerGet]:
        rows = conn.execute("SELECT * FROM explorers").fetchall()
        return [ExplorerGet(**dict(r)) for r in rows]

    @staticmethod
    def get_by_id(conn: Connection, explorer_id: int) -> Optional[ExplorerGet]:
        row = conn.execute("SELECT * FROM explorers WHERE id = ?", (explorer_id,)).fetchone()
        return ExplorerGet(**dict(row)) if row else None

    @staticmethod
    def create(conn: Connection, data: ExplorerCreate) -> ExplorerGet:
        cursor = conn.execute(
            "INSERT INTO explorers (name, rank, mission) VALUES (?, ?, ?)",
            (data.name, data.rank, data.mission)
        )
        conn.commit()
        return ExplorerGet(id=cursor.lastrowid, **data.dict())

    @staticmethod
    def update(conn: Connection, explorer_id: int, data: ExplorerCreate) -> Optional[ExplorerGet]:
        conn.execute(
            "UPDATE explorers SET name=?, rank=?, mission=? WHERE id=?",
            (data.name, data.rank, data.mission, explorer_id)
        )
        conn.commit()
        return ExplorerService.get_by_id(conn, explorer_id)

    @staticmethod
    def delete(conn: Connection, explorer_id: int) -> bool:
        result = conn.execute("DELETE FROM explorers WHERE id=?", (explorer_id,))
        conn.commit()
        return result.rowcount > 0
