"""
Repositorio para la tabla comidas_usuario
"""
from sqlalchemy.orm import Session
from app.models.comidas_usuario import ComidaUsuario


class ComidaUsuarioRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, comida_id: int, usuario_id: int, categoria_id: int | None = None) -> ComidaUsuario:
        cu = ComidaUsuario(comida_id=comida_id, usuario_id=usuario_id, categoria_id=categoria_id)
        self.db.add(cu)
        self.db.commit()
        self.db.refresh(cu)
        return cu

    def get_by_user(self, usuario_id: int):
        return (
            self.db.query(ComidaUsuario)
            .filter(ComidaUsuario.usuario_id == usuario_id)
            .all()
        )

    def delete(self, id: int) -> bool:
        cu = self.db.query(ComidaUsuario).filter(ComidaUsuario.id == id).first()
        if not cu:
            return False
        self.db.delete(cu)
        self.db.commit()
        return True
