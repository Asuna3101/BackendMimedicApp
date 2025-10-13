from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.models.appointment_reminder import AppointmentReminder

class AppointmentReminderRepository:
    def __init__(self, db: Session):
        self.db = db

    # Duplicado exacto: mismo user/doctor/hora
    def find_user_doctor_same_time(self, user_id: int, doctor_id: int, starts_at: datetime):
        return (self.db.query(AppointmentReminder)
                .filter(AppointmentReminder.user_id == user_id,
                        AppointmentReminder.doctor_id == doctor_id,
                        AppointmentReminder.starts_at == starts_at)
                .first())

    # Choque ± ventana min para el mismo doctor (cualquier usuario)
    def find_doctor_in_window(self, doctor_id: int, starts_at: datetime, window: timedelta):
        low, high = starts_at - window, starts_at + window
        return (self.db.query(AppointmentReminder)
                .filter(AppointmentReminder.doctor_id == doctor_id,
                        AppointmentReminder.starts_at.between(low, high))
                .first())

    def create(self, *, user_id: int, clinic_id: int, specialty_id: int,
               doctor_id: int, starts_at: datetime, notes: str | None):
        obj = AppointmentReminder(
            user_id=user_id,
            clinic_id=clinic_id,
            specialty_id=specialty_id,
            doctor_id=doctor_id,
            starts_at=starts_at,
            notes=notes
        )
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def list_by_user(self, user_id: int):
        return (self.db.query(AppointmentReminder)
                .filter(AppointmentReminder.user_id == user_id)
                .order_by(AppointmentReminder.starts_at.desc())
                .all())

    def get(self, reminder_id: int):
        return self.db.query(AppointmentReminder).get(reminder_id)

    def delete(self, obj: AppointmentReminder):
        self.db.delete(obj)
        self.db.commit()
