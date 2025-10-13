# app/schemas/healthcare.py
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict

# ---------- CATÁLOGOS ----------

class ClinicOut(BaseModel):
    id: int
    nombre: str
    ciudad: str | None = None
    direccion: str | None = None
    model_config = ConfigDict(from_attributes=True)   # Pydantic v2

class SpecialtyOut(BaseModel):
    id: int
    nombre: str
    model_config = ConfigDict(from_attributes=True)

class DoctorOut(BaseModel):
    id: int
    nombre: str
    clinica_id: int
    especialidad_id: int
    model_config = ConfigDict(from_attributes=True)

# ------ APPOINTMENT REMINDERS ------

# Si ya envías snake_case desde el front, NO pongas alias y deja así:
class AppointmentReminderCreate(BaseModel):
    clinic_id: int
    specialty_id: int
    doctor_id: int
    starts_at: datetime
    notes: str | None = None

# Si todavía puede llegar camelCase, usa alias (opcional):
# class AppointmentReminderCreate(BaseModel):
#     clinic_id: int      = Field(..., alias="clinicId")
#     specialty_id: int   = Field(..., alias="specialtyId")
#     doctor_id: int      = Field(..., alias="doctorId")
#     starts_at: datetime = Field(..., alias="startsAt")
#     notes: str | None = None
#     model_config = ConfigDict(populate_by_name=True)

class AppointmentReminderOut(BaseModel):
    id: int
    clinic_id: int
    specialty_id: int
    doctor_id: int
    starts_at: datetime
    notes: str | None = None
    model_config = ConfigDict(from_attributes=True)
