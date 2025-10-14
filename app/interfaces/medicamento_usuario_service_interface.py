"""
Interfaz simplificada de servicio medicamento usuario
"""
from abc import ABC, abstractmethod
from typing import Optional


class IMedicamentoUsuarioService(ABC):
    """Interfaz del servicio simplificada de servicio medicamento usuario"""
    
    @abstractmethod
    def registrar_medicamento_usuario(self, id_usuario: int, data) -> dict:
        """Registrar medicamento para un usuario"""
        pass
    
    @abstractmethod
    def obtener_medicamentos_por_usuario(self, id_usuario: int) -> Optional[list]:
        """Obtener medicamentos por usuario"""
        pass