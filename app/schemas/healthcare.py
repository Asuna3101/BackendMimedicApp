from datetime import date, time, datetime
from pydantic import BaseModel

class ClinicOut(BaseModel):
    id: int
    nombre: str
    ciudad: str | None = None
    direccion: str | None = None
    class Config: from_attributes = True

class SpecialtyOut(BaseModel):
    id: int
    nombre: str
    class Config: from_attributes = True

class DoctorOut(BaseModel):
    id: int
    nombre: str
    clinica_id: int
    especialidad_id: int
    class Config: from_attributes = True

class SlotOut(BaseModel):
    hora_inicio: time
    hora_fin: time
    disponible: bool

class AvailabilityOut(BaseModel):
    doctor_id: int
    fecha: date
    slots: list[SlotOut]

class AppointmentCreate(BaseModel):
    doctor_id: int
    fecha: date
    hora_inicio: time
    hora_fin: time

class AppointmentOut(BaseModel):
    id: int
    doctor_id: int
    paciente_id: int
    fecha: date
    hora_inicio: time
    hora_fin: time
    estado: str
    created_at: datetime
    class Config: from_attributes = True
