"""
Modelo de EjercicioUsuario
"""
from sqlalchemy import Column, Integer, ForeignKey, DateTime, String, func
from app.core.database import Base


class EjercicioUsuario(Base):
    __tablename__ = "ejercicio_usuario"

    id = Column(Integer, primary_key=True, autoincrement=True)
    idUsuario = Column(Integer, ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False)
    idEjercicio = Column(Integer, ForeignKey("ejercicios.id", ondelete="CASCADE"), nullable=False)
    
    notas = Column(String(255), nullable=True)
    horario = Column(DateTime(timezone=True), nullable=True)
    duracion_min = Column(Integer, nullable=True)  

    createdAt = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updatedAt = Column(DateTime(timezone=True), onupdate=func.now())
