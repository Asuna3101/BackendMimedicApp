from app.core.database import Base  # el ÚNICO Base

# importa todos los modelos para registrarlos en el mapper
from .user import User
from .clinic import Clinic
from .specialty import Specialty
from .doctor import Doctor
from .appointment_reminder import AppointmentReminder

