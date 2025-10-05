from sqlalchemy import Column, Integer, SmallInteger, Time, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.models.base import Base

class DoctorAvailability(Base):
    __tablename__ = "doctor_disponibilidad"

    id = Column(Integer, primary_key=True)
    doctor_id = Column(Integer, ForeignKey("doctores.id", ondelete="CASCADE"), nullable=False)
    day_of_week = Column(SmallInteger, nullable=False)  # 1=Lunes ... 6=Sábado
    hora_inicio = Column(Time, nullable=False)
    hora_fin = Column(Time, nullable=False)

    __table_args__ = (UniqueConstraint("doctor_id", "day_of_week", "hora_inicio",
                                       name="uq_doctor_dow_slot"),)

    doctor = relationship("Doctor", back_populates="disponibilidades")
