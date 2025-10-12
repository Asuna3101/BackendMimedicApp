"""
Repositorio para Citas
"""
from sqlalchemy.orm import Session
from app.interfaces.citas_repository_interface import ICitasRepository
from app.models.appointment import Appointment

from app.models.clinic import Clinic
from app.models.doctor import Doctor
from app.models.specialty import Specialty


class CitasRepository(ICitasRepository):
    def __init__(self, db: Session):
        self.db = db

    def get_by_usuario(self, id_usuario: int):
        return (
            self.db.query(Appointment, Doctor, Clinic, Specialty)
            .join(Doctor, Doctor.id == Appointment.doctor_id)
            .join(Clinic, Doctor.clinica_id == Clinic.id)
            .join(Specialty, Doctor.especialidad_id == Specialty.id)
            .filter(Appointment.paciente_id == id_usuario)
            .all()
        )