from datetime import date
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.api.deps import get_db, get_current_user

from app.models import clinic as mclinic
from app.models import specialty as mspec
from app.models import clinic_specialty as mcs
from app.models import doctor as mdoc
from app.models import doctor_availability as mdav
from app.models import appointment as mapp

from app.schemas.healthcare import (
    ClinicOut, SpecialtyOut, DoctorOut, AvailabilityOut, SlotOut,
    AppointmentCreate, AppointmentOut
)

router = APIRouter()

@router.get("/clinicas", response_model=list[ClinicOut])
def list_clinics(db: Session = Depends(get_db)):
    return db.query(mclinic.Clinic).all()

@router.get("/clinicas/{clinica_id}/especialidades", response_model=list[SpecialtyOut])
def list_specialties_by_clinic(clinica_id: int, db: Session = Depends(get_db)):
    q = (db.query(mspec.Specialty)
         .join(mcs.ClinicSpecialty, mcs.ClinicSpecialty.especialidad_id == mspec.Specialty.id)
         .filter(mcs.ClinicSpecialty.clinica_id == clinica_id))
    return q.all()

@router.get("/doctores", response_model=list[DoctorOut])
def list_doctors(clinica_id: int = Query(...), especialidad_id: int = Query(...),
                 db: Session = Depends(get_db)):
    return (db.query(mdoc.Doctor)
              .filter(and_(mdoc.Doctor.clinica_id == clinica_id,
                           mdoc.Doctor.especialidad_id == especialidad_id))
              .all())

@router.get("/doctores/{doctor_id}/availability", response_model=AvailabilityOut)
def doctor_availability(doctor_id: int, fecha: date, db: Session = Depends(get_db)):
    dow = fecha.isoweekday()  # 1..7
    if dow == 7:  # domingo: sin slots (o adapta a tu política)
        return AvailabilityOut(doctor_id=doctor_id, fecha=fecha, slots=[])

    slots = (db.query(mdav.DoctorAvailability)
               .filter(and_(mdav.DoctorAvailability.doctor_id == doctor_id,
                            mdav.DoctorAvailability.day_of_week == dow))
               .all())

    booked = {(c.hora_inicio, c.hora_fin) for c in db.query(mapp.Appointment)
                                               .filter(and_(mapp.Appointment.doctor_id == doctor_id,
                                                            mapp.Appointment.fecha == fecha)).all()}
    out = [SlotOut(hora_inicio=s.hora_inicio, hora_fin=s.hora_fin,
                   disponible=(s.hora_inicio, s.hora_fin) not in booked)
           for s in slots]
    return AvailabilityOut(doctor_id=doctor_id, fecha=fecha, slots=out)

@router.post("/citas", response_model=AppointmentOut, status_code=status.HTTP_201_CREATED)
def create_appointment(payload: AppointmentCreate,
                       db: Session = Depends(get_db),
                       user=Depends(get_current_user)):
    dow = payload.fecha.isoweekday()
    if dow == 7:
        raise HTTPException(status_code=400, detail="El domingo no se atiende")

    slot = (db.query(mdav.DoctorAvailability)
              .filter(and_(mdav.DoctorAvailability.doctor_id == payload.doctor_id,
                           mdav.DoctorAvailability.day_of_week == dow,
                           mdav.DoctorAvailability.hora_inicio == payload.hora_inicio,
                           mdav.DoctorAvailability.hora_fin == payload.hora_fin))
              .first())
    if not slot:
        raise HTTPException(status_code=400, detail="Slot inválido para este doctor")

    cita = mapp.Appointment(
        doctor_id=payload.doctor_id,
        paciente_id=user.id,
        fecha=payload.fecha,
        hora_inicio=payload.hora_inicio,
        hora_fin=payload.hora_fin,
        estado="confirmada"
    )
    db.add(cita)
    try:
        db.commit()
        db.refresh(cita)
    except Exception:
        db.rollback()
        raise HTTPException(status_code=409, detail="Horario ya reservado")
    return cita
