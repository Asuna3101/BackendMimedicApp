"""
Schemas para ejerciciosUsuario
"""
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class EjercicioUsuarioCreate(BaseModel):
    nombre: str
    notas: str
    horario: datetime
    duracion_min: int

class EjercicioUsuarioUpdate(BaseModel):
    nombre: Optional[str]
    notas: Optional[str]
    horario: Optional[datetime]
    duracion_min: Optional[int]

class EjercicioUsuarioResponse(BaseModel):
    id: int
    nombre: str
    notas: str
    horario: datetime
    duracion_min: int
    
    class Config:
        from_attributes = True