from datetime import timedelta, datetime
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.repositories.appointment_reminder_repository import AppointmentReminderRepository

WINDOW = timedelta(minutes=15)

class AppointmentReminderService:
    def __init__(self, db: Session):
        self.repo = AppointmentReminderRepository(db)

    def create(self, *, user_id: int, clinic_id: int, specialty_id: int,
               doctor_id: int, starts_at: datetime, notes: str | None):
        # Regla 1: duplicado exacto por usuario/doctor/hora
        if self.repo.find_user_doctor_same_time(user_id, doctor_id, starts_at):
            raise HTTPException(status_code=409,
                                detail="Ya registraste esa cita con ese doctor a esa hora.")

        # Regla 2: ventana ±15 min para el mismo doctor
        if self.repo.find_doctor_in_window(doctor_id, starts_at, WINDOW):
            raise HTTPException(status_code=409,
                                detail="Otra cita para el mismo doctor dentro de ±15 minutos.")

        return self.repo.create(
            user_id=user_id,
            clinic_id=clinic_id,
            specialty_id=specialty_id,
            doctor_id=doctor_id,
            starts_at=starts_at,
            notes=notes,
        )

    def list_by_user(self, *, user_id: int):
        return self.repo.list_by_user(user_id)

    def delete(self, *, user_id: int, reminder_id: int):
        obj = self.repo.get(reminder_id)
        if not obj or obj.user_id != user_id:
            raise HTTPException(status_code=404, detail="No encontrado")
        self.repo.delete(obj)
