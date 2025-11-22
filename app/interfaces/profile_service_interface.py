from abc import ABC, abstractmethod
from typing import Optional

class IProfileService(ABC):
    @abstractmethod
    def update_photo(self, user_id: int, file_path: Optional[str], url: Optional[str]) -> str:
        """Actualiza la foto de perfil y devuelve la URL"""
        raise NotImplementedError

    @abstractmethod
    def change_password(self, user_id: int, old_password: str, new_password: str) -> None:
        """Cambiar contraseña verificando la anterior"""
        raise NotImplementedError

    @abstractmethod
    def delete_account(self, user_id: int) -> None:
        """Desactivar/eliminar cuenta (soft delete)"""
        raise NotImplementedError

    @abstractmethod
    def recover_account(self, email: str) -> None:
        """Enviar instrucción de recuperación (stub)"""
        raise NotImplementedError
