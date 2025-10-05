from sqlalchemy import Column, Integer, ForeignKey, Date, Time, String, UniqueConstraint, DateTime, func
from sqlalchemy.orm import relationship
from app.models.base import Base

class Appointment(Base):
    __tablename__ = "citas"

    id = Column(Integer, primary_key=True)
    doctor_id = Column(Integer, ForeignKey("doctores.id", ondelete="CASCADE"), nullable=False, index=True)
    paciente_id = Column(Integer, ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False, index=True)

    fecha = Column(Date, nullable=False)
    hora_inicio = Column(Time, nullable=False)
    hora_fin = Column(Time, nullable=False)

    estado = Column(String(20), default="confirmada")  # confirmada/cancelada
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        UniqueConstraint("doctor_id", "fecha", "hora_inicio", name="uq_cita_doctor_slot"),
        UniqueConstraint("paciente_id", "fecha", "hora_inicio", name="uq_cita_paciente_slot"),
    )

    doctor = relationship("Doctor", back_populates="citas")
    paciente = relationship("User")  # tu modelo existente app.models.user.User
