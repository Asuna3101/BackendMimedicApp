from datetime import timedelta, datetime
from app.interfaces.appointment_reminder_repository_interface import IAppointmentReminderRepository

WINDOW = timedelta(minutes=15)       # colisión de agenda del mismo doctor ±15m
DUE_SOON_WINDOW = timedelta(minutes=30)  # “en los próximos 30m”
OVERDUE_WINDOW = timedelta(minutes=30)   # “pasadas en los últimos 30m”

def _naive(dt: datetime) -> datetime:
    return dt.replace(tzinfo=None) if (dt.tzinfo is not None and dt.tzinfo.utcoffset(dt) is not None) else dt

class AppointmentReminderService:
    def __init__(self, repo: IAppointmentReminderRepository):
        self.repo = repo

    def create(self, *, user_id: int, clinic_id: int, specialty_id: int,
               doctor_id: int, starts_at: datetime, notes: str | None):
        if self.repo.find_user_doctor_same_time(user_id, doctor_id, starts_at):
            raise ValueError("Ya registraste esa cita con ese doctor a esa hora.")
        if self.repo.find_doctor_in_window(doctor_id, starts_at, WINDOW):
            raise ValueError("Otra cita para el mismo doctor dentro de ±15 minutos.")
        return self.repo.create(
            user_id=user_id, clinic_id=clinic_id, specialty_id=specialty_id,
            doctor_id=doctor_id, starts_at=starts_at, notes=notes,
        )

    def list_upcoming(self, *, user_id: int, now: datetime):
        now_n = _naive(now)
        items = self.repo.list_upcoming_by_user(user_id, now_n)
        soon_hi = now_n + DUE_SOON_WINDOW
        for x in items:
            xs = _naive(x.starts_at)
            x.is_due_soon = (now_n <= xs <= soon_hi)
        return items

    def list_overdue(self, *, user_id: int, now: datetime):
        now_n = _naive(now)
        return self.repo.list_overdue_pending_by_user(user_id, now_n, OVERDUE_WINDOW)

    def delete(self, *, user_id: int, reminder_id: int):
        obj = self.repo.get(reminder_id)
        if not obj or obj.user_id != user_id:
            raise ValueError("No encontrado")
        self.repo.delete(obj)

    def set_status(self, *, user_id: int, reminder_id: int, status: str):
        if status not in ("PENDIENTE", "ASISTIDO", "NO_ASISTIDO"):
            raise ValueError("Estado inválido")
        obj = self.repo.get(reminder_id)
        if not obj or obj.user_id != user_id:
            raise ValueError("No encontrado")
        return self.repo.set_status(obj, status)
