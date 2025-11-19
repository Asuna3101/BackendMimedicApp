"""
Modelo unión Comida <-> Usuario (comidas_usuario)
"""
from sqlalchemy import Column, Integer, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from app.core.database import Base


class ComidaUsuario(Base):
    __tablename__ = "comidas_usuario"

    id = Column(Integer, primary_key=True, autoincrement=True)
    comida_id = Column(Integer, ForeignKey("comidas.id", ondelete="CASCADE"), nullable=False, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False, index=True)
    categoria_id = Column(Integer, ForeignKey("categorias.id", ondelete="RESTRICT"), nullable=True, index=True)

    createdAt = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updatedAt = Column(DateTime(timezone=True), onupdate=func.now())

    comida = relationship("Alimento")
    usuario = relationship("User")
    categoria = relationship("Categoria", back_populates="comidas")
