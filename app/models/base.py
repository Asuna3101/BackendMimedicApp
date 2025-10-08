"""
Base para todos los modelos
"""
from app.core.database import Base

# Importar todos los modelos aquí para que sean registrados
from app.models.user import User  # noqa
from app.models.medicamento import Medicamento
from app.models.unidad import Unidad
from app.models.medicamentoUsuario import MedicamentoUsuario
from app.models.toma import Toma
