"""
Servicio simplificado solo para autenticación
"""
from typing import Optional

from app.models.user import User
from app.interfaces.user_service_interface import IUserService
from app.interfaces.user_repository_interface import IUserRepository
from app.interfaces.auth_interface import IPasswordHasher


class UserService(IUserService):
    """Servicio simplificado solo para login"""
    
    def __init__(self, repository: IUserRepository, password_hasher: IPasswordHasher):
        self.repository = repository
        self.password_hasher = password_hasher
    
    def get_user_by_email(self, email: str) -> Optional[User]:
        """Obtener usuario por correo"""
        return self.repository.get_by_email(email)
    
    def authenticate_user(self, username_or_email: str, password: str) -> Optional[User]:
        """Autenticar usuario por correo o username"""
        # Buscar por correo (en nuestro caso, username es el correo)
        user = self.repository.get_by_email(username_or_email)
        
        # Verificar contraseña
        if not user or not self.password_hasher.verify_password(password, user.hashed_password):
            return None
        
        # Verificar que el usuario esté activo
        if not user.is_active:
            raise ValueError("Usuario inactivo")
        
        return user