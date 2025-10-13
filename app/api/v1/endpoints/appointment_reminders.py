from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.api.v1.endpoints.dependencies import get_current_user

from app.controllers.appointment_reminder_controller import AppointmentReminderController
from app.schemas.healthcare import AppointmentReminderCreate, AppointmentReminderOut

router = APIRouter(prefix="/health/appointment-reminders", tags=["citas"])

@router.post("", response_model=AppointmentReminderOut, status_code=status.HTTP_201_CREATED)
def create_appointment_reminder(payload: AppointmentReminderCreate,
                                db: Session = Depends(get_db),
                                current_user = Depends(get_current_user)):
    ctrl = AppointmentReminderController(db)
    return ctrl.crear(
        user_id=current_user.id,
        clinic_id=payload.clinic_id,
        specialty_id=payload.specialty_id,
        doctor_id=payload.doctor_id,
        starts_at=payload.starts_at,
        notes=payload.notes,
    )

@router.get("", response_model=list[AppointmentReminderOut])
def list_my_appointment_reminders(db: Session = Depends(get_db),
                                  current_user = Depends(get_current_user)):
    ctrl = AppointmentReminderController(db)
    return ctrl.listar_por_usuario(user_id=current_user.id)

@router.delete("/{reminder_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_appointment_reminder(reminder_id: int,
                                db: Session = Depends(get_db),
                                current_user = Depends(get_current_user)):
    ctrl = AppointmentReminderController(db)
    ctrl.eliminar(user_id=current_user.id, reminder_id=reminder_id)
