"""
Interfaces del repositorio - Inversión de dependencias (DIP)
"""
from abc import ABC, abstractmethod
from typing import Optional, List
from app.models.medicamentoUsuario import MedicamentoUsuario


class IMedicamentoUsuarioRepository(ABC):
    """Interfaz del repositorio de medicamentos por usuario"""

    @abstractmethod
    def create(self, medicamentoUsuario_data: dict) -> MedicamentoUsuario:
        """Crear medicamento por usuario"""
        pass
    
    @abstractmethod
    def generate_tomas(self, medxuser: MedicamentoUsuario) -> None:
        """Generar tomas para medicamento por usuario"""
        pass
    
    @abstractmethod
    def get_by_usuario(self, id_usuario: int) -> Optional[List[MedicamentoUsuario]]:
        """Obtener medicamentos por usuario"""
        pass

    @abstractmethod
    def get_by_id(self, id_medxuser: int) -> Optional[MedicamentoUsuario]:
        """Obtener un registro medicamento_usuario por su ID"""
        pass

    @abstractmethod
    def update(self, id_medxuser: int, update_data: dict) -> Optional[MedicamentoUsuario]:
        """Actualizar un registro medicamento_usuario"""
        pass