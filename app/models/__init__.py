# app/models/__init__.py
from .base import Base

# importa TODOS los modelos que deben existir en metadata:
from .user import User
from .clinic import Clinic
from .specialty import Specialty
from .clinic_specialty import ClinicSpecialty
from .doctor import Doctor
from .appointment_reminder import AppointmentReminder
# (NO importes doctor_availability ni appointment legacy si ya los eliminaste)
