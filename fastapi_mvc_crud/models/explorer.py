# models/explorer.py
from pydantic import BaseModel
from typing import Optional


class ExplorerBase(BaseModel):
    name: str
    rank: Optional[str] = None
    mission: Optional[str] = None


class ExplorerCreate(ExplorerBase):
    pass


class ExplorerGet(ExplorerBase):
    id: int

    class Config:
        from_attributes = True
