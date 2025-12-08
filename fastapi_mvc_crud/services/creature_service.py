# services/creature_service.py
from typing import List, Optional
from sqlite3 import Connection
from models.creature import CreatureCreate, CreatureGet


class CreatureService:

    @staticmethod
    def get_all(conn: Connection) -> List[CreatureGet]:
        rows = conn.execute("SELECT * FROM creatures").fetchall()
        return [CreatureGet(**dict(r)) for r in rows]

    @staticmethod
    def get_by_id(conn: Connection, creature_id: int) -> Optional[CreatureGet]:
        row = conn.execute("SELECT * FROM creatures WHERE id = ?", (creature_id,)).fetchone()
        return CreatureGet(**dict(row)) if row else None

    @staticmethod
    def create(conn: Connection, data: CreatureCreate) -> CreatureGet:
        cursor = conn.execute(
            "INSERT INTO creatures (name, habitat, power) VALUES (?, ?, ?)",
            (data.name, data.habitat, data.power)
        )
        conn.commit()
        new_id = cursor.lastrowid
        return CreatureGet(id=new_id, **data.dict())

    @staticmethod
    def update(conn: Connection, creature_id: int, data: CreatureCreate) -> Optional[CreatureGet]:
        conn.execute(
            "UPDATE creatures SET name=?, habitat=?, power=? WHERE id=?",
            (data.name, data.habitat, data.power, creature_id)
        )
        conn.commit()
        return CreatureService.get_by_id(conn, creature_id)

    @staticmethod
    def delete(conn: Connection, creature_id: int) -> bool:
        result = conn.execute("DELETE FROM creatures WHERE id=?", (creature_id,))
        conn.commit()
        return result.rowcount > 0
