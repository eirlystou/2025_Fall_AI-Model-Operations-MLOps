# models/creature.py
from pydantic import BaseModel
from typing import Optional


class CreatureBase(BaseModel):
    name: str
    habitat: Optional[str] = None
    power: Optional[int] = None


class CreatureCreate(CreatureBase):
    pass


class CreatureGet(CreatureBase):
    id: int

    class Config:
        from_attributes = True
