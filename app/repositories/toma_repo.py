"""
Repositorio para tomas
"""
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.toma import Toma


class TomaRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, toma_id: int) -> Toma | None:
        return self.db.query(Toma).filter(Toma.id == toma_id).first()

    def update_tomado(self, toma_id: int, tomado: bool) -> Toma | None:
        toma = self.get_by_id(toma_id)
        if not toma:
            return None
        toma.tomado = tomado
        # updatedAt se actualiza por onupdate=func.now() en el modelo
        self.db.commit()
        self.db.refresh(toma)
        return toma

    def count_pendientes_by_medxuser(self, medxuser_id: int) -> int:
        return (
            self.db.query(func.count(Toma.id))
            .filter(Toma.idMedxUser == medxuser_id, Toma.tomado.is_(False))
            .scalar()
        )

    def delete_all_by_medxuser(self, medxuser_id: int) -> int:
        deleted = (
            self.db.query(Toma)
            .filter(Toma.idMedxUser == medxuser_id)
            .delete(synchronize_session=False)
        )
        self.db.commit()
        return deleted
