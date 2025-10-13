from datetime import datetime
from pydantic import BaseModel

# -------------------------- CATÁLOGOS --------------------------

class ClinicOut(BaseModel):
    id: int
    nombre: str
    ciudad: str | None = None
    direccion: str | None = None

    class Config:
        from_attributes = True  # Pydantic v2

class SpecialtyOut(BaseModel):
    id: int
    nombre: str

    class Config:
        from_attributes = True

class DoctorOut(BaseModel):
    id: int
    nombre: str
    clinica_id: int
    especialidad_id: int

    class Config:
        from_attributes = True


# -------------------- APPOINTMENT REMINDERS --------------------

class AppointmentReminderCreate(BaseModel):
    clinic_id: int
    specialty_id: int
    doctor_id: int
    starts_at: datetime          # fecha+hora (ISO 8601)
    notes: str | None = None

class AppointmentReminderOut(BaseModel):
    id: int
    clinic_id: int
    specialty_id: int
    doctor_id: int
    starts_at: datetime
    notes: str | None = None

    class Config:
        from_attributes = True
