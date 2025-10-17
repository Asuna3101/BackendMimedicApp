from datetime import datetime, timedelta
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_
from app.models.appointment_reminder import AppointmentReminder

class AppointmentReminderRepository:
    def __init__(self, db: Session):
        self.db = db

    def find_user_doctor_same_time(self, user_id: int, doctor_id: int, starts_at: datetime):
        return (
            self.db.query(AppointmentReminder)
            .filter(
                AppointmentReminder.user_id == user_id,
                AppointmentReminder.doctor_id == doctor_id,
                AppointmentReminder.starts_at == starts_at,
            )
            .first()
        )

    def find_doctor_in_window(self, doctor_id: int, starts_at: datetime, window: timedelta):
        low, high = starts_at - window, starts_at + window
        return (
            self.db.query(AppointmentReminder)
            .filter(
                AppointmentReminder.doctor_id == doctor_id,
                AppointmentReminder.starts_at.between(low, high),
            )
            .first()
        )

    def create(
        self,
        *,
        user_id: int,
        clinic_id: int,
        specialty_id: int,
        doctor_id: int,
        starts_at: datetime,
        notes: str | None,
    ):
        obj = AppointmentReminder(
            user_id=user_id,
            clinic_id=clinic_id,
            specialty_id=specialty_id,
            doctor_id=doctor_id,
            starts_at=starts_at,
            notes=notes,
            status="PENDIENTE",
        )
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        # recarga con relaciones
        obj = (
            self.db.query(AppointmentReminder)
            .options(
                joinedload(AppointmentReminder.clinic),
                joinedload(AppointmentReminder.specialty),
                joinedload(AppointmentReminder.doctor),
            )
            .get(obj.id)
        )
        return obj

    def list_upcoming_by_user(self, user_id: int, now: datetime):
        q = (
            self.db.query(AppointmentReminder)
            .options(
                joinedload(AppointmentReminder.clinic),
                joinedload(AppointmentReminder.specialty),
                joinedload(AppointmentReminder.doctor),
            )
            .filter(
                AppointmentReminder.user_id == user_id,
                AppointmentReminder.status == "PENDIENTE",
                AppointmentReminder.starts_at >= now,
            )
            .order_by(AppointmentReminder.starts_at.asc())
        )
        return q.all()

    def list_overdue_pending_by_user(self, user_id: int, now: datetime, window: timedelta):
        low = now - window
        q = (
            self.db.query(AppointmentReminder)
            .options(
                joinedload(AppointmentReminder.clinic),
                joinedload(AppointmentReminder.specialty),
                joinedload(AppointmentReminder.doctor),
            )
            .filter(
                and_(
                    AppointmentReminder.user_id == user_id,
                    AppointmentReminder.status == "PENDIENTE",
                    AppointmentReminder.starts_at < now,
                    AppointmentReminder.starts_at >= low,
                )
            )
            .order_by(AppointmentReminder.starts_at.desc())
        )
        return q.all()

    def get(self, reminder_id: int):
        return self.db.get(AppointmentReminder, reminder_id)

    def set_status(self, obj: AppointmentReminder, status: str):
        obj.status = status
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def delete(self, obj: AppointmentReminder):
        self.db.delete(obj)
        self.db.commit()
