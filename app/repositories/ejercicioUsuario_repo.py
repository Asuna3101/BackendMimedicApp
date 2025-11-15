"""
Repositorio para EjercicioUsuario
"""
from sqlalchemy import desc
from sqlalchemy.orm import Session
from app.models.ejercicio import Ejercicio
from app.models.ejercicioUsuario import EjercicioUsuario
from app.interfaces.ejercicio_usuario_repository_interface import IEjercicioUsuarioRepository


class EjercicioUsuarioRepository(IEjercicioUsuarioRepository):

    def __init__(self, db: Session):
        self.db = db

    def create(self, data: dict) -> EjercicioUsuario:
        ejxuser = EjercicioUsuario(**data)
        self.db.add(ejxuser)
        self.db.commit()
        self.db.refresh(ejxuser)
        return ejxuser

    def get_by_usuario(self, id_usuario: int):
        return (
            self.db.query(EjercicioUsuario, Ejercicio)
            .join(Ejercicio, Ejercicio.id == EjercicioUsuario.idEjercicio)
            .filter(EjercicioUsuario.idUsuario == id_usuario)
            .order_by(desc(EjercicioUsuario.createdAt))
            .all()
        )

    def update(self, ejercicio_id: int, data: dict):
        ejxuser = (
            self.db.query(EjercicioUsuario)
            .filter(EjercicioUsuario.id == ejercicio_id)
            .first()
        )
        if not ejxuser:
            return None

        for field, value in data.items():
            setattr(ejxuser, field, value)

        self.db.commit()
        self.db.refresh(ejxuser)
        return ejxuser

    def delete(self, ejercicio_id: int) -> bool:
        ejxuser = (
            self.db.query(EjercicioUsuario)
            .filter(EjercicioUsuario.id == ejercicio_id)
            .first()
        )
        if not ejxuser:
            return False

        self.db.delete(ejxuser)
        self.db.commit()
        return True