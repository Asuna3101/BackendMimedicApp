"""
Base para todos los modelos
"""
from app.core.database import Base

# Importar todos los modelos aquí para que sean registrados
from app.models.user import User  # noqa