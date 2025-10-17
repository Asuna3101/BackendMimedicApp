from datetime import datetime
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.factories.service_factory import ServiceFactory
from app.schemas.healthcare import AppointmentReminderCreate

class AppointmentReminderController:
    def __init__(self, db: Session):
        repo = ServiceFactory.create_appointment_reminder_repository(db)
        self.svc = ServiceFactory.create_appointment_reminder_service(repo)

    def create(self, user_id: int, data: AppointmentReminderCreate):
        try:
            return self.svc.create(
                user_id=user_id,
                clinic_id=data.clinic_id,
                specialty_id=data.specialty_id,
                doctor_id=data.doctor_id,
                starts_at=data.starts_at,  # local (sin tz)
                notes=data.notes,
            )
        except ValueError as e:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error al crear cita: {e}")

    def list_upcoming(self, user_id: int, now: datetime):
        return self.svc.list_upcoming(user_id=user_id, now=now)

    def list_overdue(self, user_id: int, now: datetime):
        return self.svc.list_overdue(user_id=user_id, now=now)

    def set_status(self, user_id: int, reminder_id: int, status: str):
        try:
            self.svc.set_status(user_id=user_id, reminder_id=reminder_id, status=status)
        except ValueError as e:
            msg = str(e).lower()
            code = status.HTTP_404_NOT_FOUND if "no encontrado" in msg else status.HTTP_400_BAD_REQUEST
            raise HTTPException(status_code=code, detail=str(e))

    def delete(self, user_id: int, reminder_id: int):
        try:
            self.svc.delete(user_id=user_id, reminder_id=reminder_id)
        except ValueError as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
