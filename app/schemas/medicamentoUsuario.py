"""
Schemas para registro de medicamentos asociados a usuarios
"""
from pydantic import BaseModel, ConfigDict
from datetime import datetime


class MedicamentoUsuarioCreate(BaseModel):
    nombre: str
    dosis: int
    unidad: str
    frecuencia_horas: int
    fecha_inicio: datetime
    fecha_fin: datetime

