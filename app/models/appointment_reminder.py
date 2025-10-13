# app/models/appointment_reminder.py
from sqlalchemy import Column, Integer, ForeignKey, DateTime, String, UniqueConstraint
from sqlalchemy.orm import relationship
from app.models.base import Base   # re-exporta el Base real aquí (ver punto 2)

class AppointmentReminder(Base):
    __tablename__ = "appointment_reminders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False, index=True)

    clinic_id = Column(Integer, ForeignKey("clinicas.id"), nullable=False)
    specialty_id = Column(Integer, ForeignKey("especialidades.id"), nullable=False)
    doctor_id = Column(Integer, ForeignKey("doctores.id"), nullable=False, index=True)

    starts_at = Column(DateTime, nullable=False, index=True)
    notes = Column(String(400), nullable=True)

    __table_args__ = (
        UniqueConstraint("user_id", "doctor_id", "starts_at", name="uq_user_doctor_start"),
    )

    clinic = relationship("Clinic")
    specialty = relationship("Specialty")
    doctor = relationship("Doctor")
