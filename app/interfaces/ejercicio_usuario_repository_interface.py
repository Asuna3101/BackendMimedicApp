"""
Interfaces del repositorio 
"""
from abc import ABC, abstractmethod
from typing import Optional, List

from app.models.ejercicioUsuario import EjercicioUsuario


class IEjercicioUsuarioRepository(ABC):
    """Interfaz del repositorio de ejercicios por usuario"""

    @abstractmethod
    def create(self, data: dict) -> EjercicioUsuario:
        """Crear ejercicio por usuario"""
        pass
    
    @abstractmethod
    def get_by_usuario(self, id_usuario: int) -> Optional[List[EjercicioUsuario]]:
        """Obtener ejercicios por usuario"""
        pass

    # posiblemente se borre
    # @abstractmethod
    # def get_by_id(self, id_ejxuser: int) -> Optional[EjercicioUsuario]:
    #     """Obtener un registro ejercicio_usuario por su ID"""
    #     pass

    @abstractmethod
    def update(self, id_ejxuser: int, data: dict) -> Optional[EjercicioUsuario]:
        """Actualizar un registro ejercicio_usuario"""
        pass

    @abstractmethod
    def delete(self, id_usuario: int, id_ejxuser: int) -> bool:
        """Eliminar un registro ejercicio_usuario si pertenece al usuario.
        """
        pass