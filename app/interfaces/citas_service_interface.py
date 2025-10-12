"""
Interfaz simplificada de servicio de citas
"""
from abc import ABC, abstractmethod
from typing import Optional


class ICitasService(ABC):
    """Interfaz del servicio simplificada de citas"""
    
    @abstractmethod
    def obtener_citas_por_usuario(self, id_usuario: int) -> Optional[list]:
        """Obtener citas por usuario"""
        pass