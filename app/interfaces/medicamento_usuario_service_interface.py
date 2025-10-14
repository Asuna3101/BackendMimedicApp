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

    @abstractmethod
    def actualizar_medicamento_usuario(self, id_usuario: int, id_medicamento_usuario: int, data) -> dict:
        """Actualizar un registro de medicamento asociado a un usuario en la base de datos.

        Args:
            id_usuario (int): ID del usuario propietario del registro.
            id_medicamento_usuario (int): ID del registro medicamento_usuario a actualizar.
            data: Diccionario o esquema (p.ej. `MedicamentoUsuarioCreate` parcial) con los campos a actualizar.

        Returns:
            dict: Representación del medicamento_usuario actualizado o información sobre la operación.
        """
        pass