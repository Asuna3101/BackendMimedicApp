"""
Repositorio para medicamentos (catálogo global)
"""
from sqlalchemy.orm import Session
from app.models.medicamento import Medicamento


class MedicamentoRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_nombre(self, nombre: str) -> Medicamento | None:
        return self.db.query(Medicamento).filter(Medicamento.nombre == nombre).first()

    def get_or_create_medicamento(self, nombre: str) -> Medicamento:
        med = self.get_by_nombre(nombre)
        if not med:
            med = Medicamento(nombre=nombre)
            self.db.add(med)
            self.db.commit()
            self.db.refresh(med)
        return med
    
    def get_all(self):
        return self.db.query(Medicamento).order_by(Medicamento.nombre.asc()).all()