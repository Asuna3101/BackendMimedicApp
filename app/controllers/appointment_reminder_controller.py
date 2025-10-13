# app/api/v1/endpoints/appointment_reminders.py
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from datetime import timezone

from app.core.database import get_db
from app.api.v1.endpoints.dependencies import get_current_user
from app.services.appointment_reminder_service import AppointmentReminderService
from app.schemas.healthcare import AppointmentReminderCreate, AppointmentReminderOut

router = APIRouter(prefix="/health/appointment-reminders", tags=["citas"])

def _svc(db: Session) -> AppointmentReminderService:
    return AppointmentReminderService(db)

@router.post("", response_model=AppointmentReminderOut, status_code=status.HTTP_201_CREATED)
def create_appointment_reminder(
    payload: AppointmentReminderCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
):
    # Normaliza a UTC y haz naive si tu columna es "timestamp without time zone"
    starts_at = payload.starts_at
    if starts_at.tzinfo is None:
        # asume que el cliente te envía UTC ya; si no, ajusta según tu TZ
        starts_at = starts_at.replace(tzinfo=timezone.utc)
    else:
        starts_at = starts_at.astimezone(timezone.utc)
    starts_at = starts_at.replace(tzinfo=None)  # columna sin tz

    return _svc(db).create(
        user_id=current_user.id,
        clinic_id=payload.clinic_id,
        specialty_id=payload.specialty_id,
        doctor_id=payload.doctor_id,
        starts_at=starts_at,
        notes=payload.notes,
    )

@router.get("", response_model=list[AppointmentReminderOut])
def list_my_appointment_reminders(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
):
    return _svc(db).list_by_user(user_id=current_user.id)

@router.delete("/{reminder_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_appointment_reminder(
    reminder_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
):
    _svc(db).delete(user_id=current_user.id, reminder_id=reminder_id)
