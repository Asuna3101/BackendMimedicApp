from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ComidaOut(BaseModel):
    """Schema para el catálogo de comidas (sin info de usuario)"""
    id: int
    nombre: str
    detalles: Optional[str] = None
    createdAt: Optional[datetime] = None

    class Config:
        from_attributes = True


class ComidaCreate(BaseModel):
    """Crear una comida en el catálogo"""
    nombre: str
    detalles: Optional[str] = None


class ComidaUsuarioCreate(BaseModel):
    """Asociar una comida del catálogo a un usuario con categoría"""
    nombre: str
    detalles: Optional[str] = None
    idCategoria: Optional[int] = None  # 1=Recomendable, 2=No Recomendable


class ComidaUsuarioResponse(BaseModel):
    """Respuesta de comida asociada a usuario"""
    id: int
    comida_id: int
    usuario_id: int
    categoria_id: Optional[int] = None
    nombre: str  # del catálogo
    detalles: str  # del catálogo
    categoria_nombre: Optional[str] = None
    createdAt: Optional[datetime] = None

    class Config:
        from_attributes = True


class ComidaUsuarioDeleteMultiple(BaseModel):
    """Eliminar múltiples comidas de usuario"""
    ids: list[int]
