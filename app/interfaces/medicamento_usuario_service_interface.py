"""
Interfaz simplificada de servicio medicamento usuario
"""
from abc import ABC, abstractmethod
from typing import Optional, List


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

    @abstractmethod
    def eliminar_medicamento_usuario(self, id_usuario: int, id_medicamento_usuario: int) -> bool:
        """Eliminar un registro medicamento-usuario si pertenece al usuario.

        Args:
            id_usuario (int): ID del usuario que solicita la eliminación.
            id_medicamento_usuario (int): ID del registro a eliminar.

        Returns:
            bool: True si se eliminó correctamente, False si no existía o no pertenece.
        """
        pass

    @abstractmethod
    def eliminar_lista_medicamento_usuario(self, id_usuario: int, ids: List[int]) -> dict:
        """Eliminar múltiples registros medicamento-usuario por sus IDs.

        Args:
            id_usuario (int): ID del usuario que solicita la eliminación.
            ids (List[int]): Lista de IDs de `medicamento_usuario` a eliminar.

        Returns:
            dict: Resumen con conteo y listas: {deleted_count, deleted_ids, failed_ids}.
        """
        pass