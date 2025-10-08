"""
Servicio de catálogo de medicamentos
"""
from app.repositories.medicamento_repo import MedicamentoRepository


class MedicamentoService:
    def __init__(self, med_repo: MedicamentoRepository):
        self.med_repo = med_repo

    def get_or_create(self, nombre: str):
        return self.med_repo.get_or_create_medicamento(nombre)
    
    def listar_todos(self):
        meds = self.med_repo.get_all()
        return [{"id": m.id, "nombre": m.nombre} for m in meds]
