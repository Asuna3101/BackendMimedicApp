"""
Interfaz del repositorio de tomas - Inversión de dependencias (DIP)
"""
from abc import ABC, abstractmethod
from typing import Optional
from app.models.toma import Toma


class ITomaRepository(ABC):
    """Interfaz del repositorio de tomas"""

    @abstractmethod
    def get_by_id(self, toma_id: int) -> Optional[Toma]:
        """Obtener toma por ID"""
        pass

    @abstractmethod
    def update_tomado(self, toma_id: int, tomado: bool) -> Optional[Toma]:
        """Actualizar el estado de una toma (tomado o no tomado)"""
        pass

    @abstractmethod
    def count_pendientes_by_medxuser(self, medxuser_id: int) -> int:
        """Contar tomas pendientes por medicamento-usuario"""
        pass

    @abstractmethod
    def delete_all_by_medxuser(self, medxuser_id: int) -> int:
        """Eliminar todas las tomas asociadas a un medicamento-usuario"""
        pass
