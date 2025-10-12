"""
Repositorio para MedicamentoUsuario
"""
from sqlalchemy.orm import Session
from app.models.medicamento import Medicamento
from app.models.medicamentoUsuario import MedicamentoUsuario
from app.models.toma import Toma
from datetime import timedelta

from app.models.unidad import Unidad


class MedicamentoUsuarioRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, medicamentoUsuario_data: dict) -> MedicamentoUsuario:
        medxuser = MedicamentoUsuario(**medicamentoUsuario_data)
        self.db.add(medxuser)
        self.db.commit()
        self.db.refresh(medxuser)
        return medxuser

    def generate_tomas(self, medxuser: MedicamentoUsuario):
        """Genera tomas cada 'frecuencia_horas' entre [fecha_inicio, fecha_fin]."""
        fecha_actual = medxuser.fecha_inicio
        delta = timedelta(hours=medxuser.frecuencia_horas)

        while fecha_actual <= medxuser.fecha_fin:
            toma = Toma(
                idMedxUser=medxuser.id,
                tomado=False,
                adquired=fecha_actual
            )
            self.db.add(toma)
            fecha_actual += delta

        self.db.commit()
    def get_by_usuario(self, id_usuario: int):
        return (
            self.db.query(MedicamentoUsuario, Medicamento, Unidad)
            .join(Medicamento, Medicamento.id == MedicamentoUsuario.idMedicamento)
            .join(Unidad, Unidad.id == MedicamentoUsuario.idUnidad)
            .filter(MedicamentoUsuario.idUsuario == id_usuario)
            .all()
        )
