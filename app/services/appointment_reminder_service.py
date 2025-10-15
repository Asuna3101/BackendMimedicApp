from datetime import timedelta, datetime
from fastapi import HTTPException
from app.repositories.appointment_reminder_repo import AppointmentReminderRepository, DUE_SOON_WINDOW

WINDOW = timedelta(minutes=15)

def _naive(dt: datetime) -> datetime:
    # Quita tz si viene aware; si ya es naive, lo deja igual
    return dt.replace(tzinfo=None) if (dt.tzinfo is not None and dt.tzinfo.utcoffset(dt) is not None) else dt

class AppointmentReminderService:
    def __init__(self, db):
        self.repo = AppointmentReminderRepository(db)

    def create(self, *, user_id: int, clinic_id: int, specialty_id: int,
               doctor_id: int, starts_at: datetime, notes: str | None):
        if self.repo.find_user_doctor_same_time(user_id, doctor_id, starts_at):
            raise HTTPException(status_code=409, detail="Ya registraste esa cita con ese doctor a esa hora.")
        if self.repo.find_doctor_in_window(doctor_id, starts_at, WINDOW):
            raise HTTPException(status_code=409, detail="Otra cita para el mismo doctor dentro de ±15 minutos.")
        return self.repo.create(
            user_id=user_id, clinic_id=clinic_id, specialty_id=specialty_id,
            doctor_id=doctor_id, starts_at=starts_at, notes=notes,
        )

    def list_upcoming(self, *, user_id: int, now: datetime):
        # Asegura coherencia: comparaciones en naive/local
        now_n = _naive(now)
        items = self.repo.list_upcoming_by_user(user_id, now_n)
        soon_hi = now_n + DUE_SOON_WINDOW
        for x in items:
            xs = _naive(x.starts_at)
            x.is_due_soon = (now_n <= xs <= soon_hi)
        return items

    def list_history(self, *, user_id: int, now: datetime):
        # Por consistencia, pasa naive al repo también
        return self.repo.list_history_by_user(user_id, _naive(now))

    def delete(self, *, user_id: int, reminder_id: int):
        obj = self.repo.get(reminder_id)
        if not obj or obj.user_id != user_id:
            raise HTTPException(status_code=404, detail="No encontrado")
        self.repo.delete(obj)

    def set_status(self, *, user_id: int, reminder_id: int, status: str):
        if status not in ("PENDIENTE", "ASISTIDO", "NO_ASISTIDO"):
            raise HTTPException(status_code=400, detail="Estado inválido")
        obj = self.repo.get(reminder_id)
        if not obj or obj.user_id != user_id:
            raise HTTPException(status_code=404, detail="No encontrado")
        return self.repo.set_status(obj, status)
