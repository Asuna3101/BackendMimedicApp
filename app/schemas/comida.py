from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ComidaOut(BaseModel):
    id: int
    nombre: str
    detalles: Optional[str] = None
    recomendable: int
    createdAt: Optional[datetime]

    class Config:
        orm_mode = True


class ComidaCreate(BaseModel):
    nombre: str
    detalles: Optional[str] = None
    recomendable: Optional[int] = 1
    idCategoria: Optional[int] = None
