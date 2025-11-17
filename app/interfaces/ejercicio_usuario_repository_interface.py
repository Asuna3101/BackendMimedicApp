"""
Interfaces del repositorio 
"""
from abc import ABC, abstractmethod
from typing import Optional, List
from datetime import time
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

    @abstractmethod
    def get_by_id(self, ejercicio_id: int) -> Optional[EjercicioUsuario]:
        """Obtener un ejercicio_usuario por ID"""
        pass

    @abstractmethod
    def update(self, id_ejxuser: int, data: dict) -> EjercicioUsuario:
        """Actualizar un registro ejercicio_usuario"""
        pass

    @abstractmethod
    def delete(self, id_usuario: int, ejercicio_ids: list[int]) -> bool:
        """Eliminar registros ejercicio_usuario"""
        pass

    @abstractmethod
    def check_horario_conflict(self, id_usuario: int, horario: time, duracion_min: int, exclude_id: int = None) -> bool:
        """Verificar si hay conflicto de horarios"""
        pass