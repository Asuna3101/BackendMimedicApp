"""
Schemas para ejerciciosUsuario
"""
from pydantic import BaseModel
from datetime import time
from typing import Optional

class EjercicioUsuarioCreate(BaseModel):
    nombre: str
    notas: str
    horario: time 
    duracion_min: int

class EjercicioUsuarioUpdate(BaseModel):
    nombre: Optional[str] = None
    notas: Optional[str] = None
    horario: Optional[time] = None 
    duracion_min: Optional[int] = None

class EjercicioUsuarioResponse(BaseModel):
    id: int
    nombre: str
    notas: str
    horario: time 
    duracion_min: int
    
    class Config:
        from_attributes = True

class EjercicioUsuarioDeleteMultiple(BaseModel):
    ids: list[int]