# routers/explorer.py
from fastapi import APIRouter, Depends, HTTPException
from data.database import get_db_connection
from models.explorer import ExplorerCreate, ExplorerGet
from services.explorer_service import ExplorerService

router = APIRouter(prefix="/explorers", tags=["Explorers"])


@router.get("/", response_model=list[ExplorerGet])
def get_all(conn=Depends(get_db_connection)):
    return ExplorerService.get_all(conn)


@router.get("/{explorer_id}", response_model=ExplorerGet)
def get_one(explorer_id: int, conn=Depends(get_db_connection)):
    explorer = ExplorerService.get_by_id(conn, explorer_id)
    if not explorer:
        raise HTTPException(status_code=404, detail="Explorer not found")
    return explorer


@router.post("/", response_model=ExplorerGet, status_code=201)
def create(data: ExplorerCreate, conn=Depends(get_db_connection)):
    return ExplorerService.create(conn, data)


@router.put("/{explorer_id}", response_model=ExplorerGet)
def update(explorer_id: int, data: ExplorerCreate, conn=Depends(get_db_connection)):
    updated = ExplorerService.update(conn, explorer_id, data)
    if not updated:
        raise HTTPException(status_code=404, detail="Explorer not found")
    return updated


@router.delete("/{explorer_id}", status_code=204)
def delete(explorer_id: int, conn=Depends(get_db_connection)):
    ok = ExplorerService.delete(conn, explorer_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Explorer not found")
