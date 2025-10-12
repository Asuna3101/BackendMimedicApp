"""
Interfaces del repositorio - Inversión de dependencias (DIP)
"""
from abc import ABC, abstractmethod
from typing import Optional, List
from app.models.appointment import Appointment


class ICitasRepository(ABC):
    """Interfaz del repositorio de citas"""
    
    @abstractmethod
    def get_by_usuario(self, id_usuario: int) -> Optional[List[Appointment]]:
        """Obtener citas por usuario"""
        pass