from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict

class ClinicOut(BaseModel):
    id: int
    nombre: str
    model_config = ConfigDict(from_attributes=True)

class SpecialtyOut(BaseModel):
    id: int
    nombre: str
    model_config = ConfigDict(from_attributes=True)

class DoctorOut(BaseModel):
    id: int
    nombre: str
    model_config = ConfigDict(from_attributes=True)

class AppointmentReminderCreate(BaseModel):
    clinic_id: int
    specialty_id: int
    doctor_id: int
    starts_at: datetime
    notes: str | None = None

class AppointmentReminderOut(BaseModel):
    id: int
    starts_at: datetime
    notes: str | None = None
    clinic: ClinicOut
    specialty: SpecialtyOut
    doctor: DoctorOut
    model_config = ConfigDict(from_attributes=True)
