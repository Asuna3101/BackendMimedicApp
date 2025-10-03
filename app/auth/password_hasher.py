"""
Implementación simple de hasheo de contraseñas
"""
import hashlib
from app.interfaces.auth_interface import IPasswordHasher
from app.core.config import settings


class SimplePasswordHasher(IPasswordHasher):
    """Implementación simple de hasheo con SHA256"""
    
    def hash_password(self, password: str) -> str:
        """Hashear contraseña con SHA256 simple"""
        salt = settings.SECRET_KEY[:16]  # Usar parte del secret key como salt
        return hashlib.sha256((password + salt).encode()).hexdigest()
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verificar contraseña con hash simple"""
        return self.hash_password(plain_password) == hashed_password


# Alias para mantener compatibilidad
BcryptPasswordHasher = SimplePasswordHasher