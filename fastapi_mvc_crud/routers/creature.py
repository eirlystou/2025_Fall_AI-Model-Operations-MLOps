# routers/creature.py
from fastapi import APIRouter, Depends, HTTPException
from data.database import get_db_connection
from models.creature import CreatureCreate, CreatureGet
from services.creature_service import CreatureService

router = APIRouter(prefix="/creatures", tags=["Creatures"])


@router.get("/", response_model=list[CreatureGet])
def get_all(conn=Depends(get_db_connection)):
    return CreatureService.get_all(conn)


@router.get("/{creature_id}", response_model=CreatureGet)
def get_one(creature_id: int, conn=Depends(get_db_connection)):
    creature = CreatureService.get_by_id(conn, creature_id)
    if not creature:
        raise HTTPException(status_code=404, detail="Creature not found")
    return creature


@router.post("/", response_model=CreatureGet, status_code=201)
def create(data: CreatureCreate, conn=Depends(get_db_connection)):
    return CreatureService.create(conn, data)


@router.put("/{creature_id}", response_model=CreatureGet)
def update(creature_id: int, data: CreatureCreate, conn=Depends(get_db_connection)):
    updated = CreatureService.update(conn, creature_id, data)
    if not updated:
        raise HTTPException(status_code=404, detail="Creature not found")
    return updated


@router.delete("/{creature_id}", status_code=204)
def delete(creature_id: int, conn=Depends(get_db_connection)):
    ok = CreatureService.delete(conn, creature_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Creature not found")
