from sqlalchemy.orm import Session
from datetime import datetime
from app.services.appointment_reminder_service import AppointmentReminderService

class AppointmentReminderController:
    def __init__(self, db: Session):
        self.svc = AppointmentReminderService(db)

    def crear(self, *, user_id: int, clinic_id: int, specialty_id: int,
              doctor_id: int, starts_at: datetime, notes: str | None):
        return self.svc.create(
            user_id=user_id,
            clinic_id=clinic_id,
            specialty_id=specialty_id,
            doctor_id=doctor_id,
            starts_at=starts_at,
            notes=notes,
        )

    def listar_por_usuario(self, *, user_id: int):
        return self.svc.list_by_user(user_id=user_id)

    def eliminar(self, *, user_id: int, reminder_id: int):
        return self.svc.delete(user_id=user_id, reminder_id=reminder_id)
