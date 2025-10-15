# app/api/v1/endpoints/appointment_reminders.py
from datetime import datetime
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.api.v1.endpoints.dependencies import get_current_user
from app.services.appointment_reminder_service import AppointmentReminderService
from app.schemas.healthcare import (
    AppointmentReminderCreate,
    AppointmentReminderOut,
    StatusIn,
)

router = APIRouter(prefix="/health/appointment-reminders", tags=["citas"])


def _svc(db: Session) -> AppointmentReminderService:
    return AppointmentReminderService(db)


@router.post("", response_model=AppointmentReminderOut, status_code=status.HTTP_201_CREATED)
def create_appointment_reminder(
    payload: AppointmentReminderCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    # starts_at debe llegar en ISO8601; asegúrate de ser consistente con lo que guarda la DB
    return _svc(db).create(
        user_id=current_user.id,
        clinic_id=payload.clinic_id,
        specialty_id=payload.specialty_id,
        doctor_id=payload.doctor_id,
        starts_at=payload.starts_at,
        notes=payload.notes,
    )


@router.get("/upcoming", response_model=list[AppointmentReminderOut])
def list_upcoming(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    now = datetime.now()
    return _svc(db).list_upcoming(user_id=current_user.id, now=now)


@router.get("/history", response_model=list[AppointmentReminderOut])
def list_history(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    now = datetime.now()
    return _svc(db).list_history(user_id=current_user.id, now=now)


@router.patch("/{reminder_id}/status", status_code=status.HTTP_204_NO_CONTENT)
def set_status(
    reminder_id: int,
    payload: StatusIn,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    _svc(db).set_status(user_id=current_user.id, reminder_id=reminder_id, status=payload.status)
    return
