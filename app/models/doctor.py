from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base

class Doctor(Base):
    __tablename__ = "doctores"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(120), nullable=False)

    clinica_id = Column(Integer, ForeignKey("clinicas.id", ondelete="CASCADE"), nullable=False)
    especialidad_id = Column(Integer, ForeignKey("especialidades.id", ondelete="CASCADE"), nullable=False)

    clinica = relationship("Clinic", back_populates="doctores")
    especialidad = relationship("Specialty")
    disponibilidades = relationship("DoctorAvailability", back_populates="doctor", cascade="all, delete")
    citas = relationship("Appointment", back_populates="doctor", cascade="all, delete")
