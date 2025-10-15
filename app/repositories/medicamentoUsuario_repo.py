"""
Repositorio para MedicamentoUsuario
"""
from sqlalchemy import desc
from sqlalchemy.orm import Session
from app.interfaces.medicamento_usuario_repository_interface import IMedicamentoUsuarioRepository
from app.models.medicamento import Medicamento
from app.models.medicamentoUsuario import MedicamentoUsuario
from app.models.toma import Toma
from datetime import timedelta

from app.models.unidad import Unidad


class MedicamentoUsuarioRepository(IMedicamentoUsuarioRepository):
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
            .order_by(desc(MedicamentoUsuario.createdAt))
            .all()
        )

    def get_by_id(self, id_medxuser: int) -> MedicamentoUsuario | None:
        return self.db.query(MedicamentoUsuario).filter(MedicamentoUsuario.id == id_medxuser).first()

    def update(self, id_medxuser: int, update_data: dict) -> MedicamentoUsuario | None:
        """Actualizar campos del registro MedicamentoUsuario"""
        medxuser = self.get_by_id(id_medxuser)
        if not medxuser:
            return None

        for field, value in update_data.items():
            # Ignorar claves no existentes
            if hasattr(medxuser, field):
                setattr(medxuser, field, value)

        self.db.commit()
        self.db.refresh(medxuser)
        return medxuser

    def delete(self, id_usuario: int, id_medxuser: int) -> bool:
        """Eliminar un registro MedicamentoUsuario y sus tomas si pertenece al usuario.

        Devuelve True si se eliminó correctamente, False si no existe o no pertenece al usuario.
        """
        medxuser = self.get_by_id(id_medxuser)
        if not medxuser:
            return False

        # Verificar pertenencia
        if medxuser.idUsuario != id_usuario:
            return False

        # Eliminar tomas asociadas
        self.db.query(Toma).filter(Toma.idMedxUser == id_medxuser).delete()

        # Eliminar el registro medxuser
        self.db.delete(medxuser)
        self.db.commit()
        return True
