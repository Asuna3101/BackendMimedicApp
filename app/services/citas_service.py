"""
Servicio para registrar citas
"""

from datetime import datetime
from app.interfaces.citas_repository_interface import ICitasRepository
from app.interfaces.citas_service_interface import ICitasService

class CitasService(ICitasService):
    def __init__(
        self,
        citas_repo: ICitasRepository,
    ):
        self.citas_repo = citas_repo

    def obtener_citas_por_usuario(self, id_usuario: int):
        rows = self.citas_repo.get_by_usuario(id_usuario)
        result = [
            {
                "id": appointment.id,
                "clinica": clinic.nombre,
                "especialidad": spec.nombre,
                "doctor": doc.nombre,
                "fecha": datetime.combine(appointment.fecha, appointment.hora_inicio),
            }
            for appointment, doc, clinic, spec in rows
        ]
        return result
