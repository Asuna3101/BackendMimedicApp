"""
Utilidades de seguridad simplificadas
"""
import hashlib
from datetime import datetime, timedelta
from typing import Any, Union
from jose import jwt

from app.core.config import settings


def create_access_token(subject: Union[str, Any], expires_delta: timedelta = None) -> str:
    """
    Crear token JWT de acceso
    """
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verificar contraseña con hash simple
    """
    return get_password_hash(plain_password) == hashed_password


def get_password_hash(password: str) -> str:
    """
    Generar hash simple de contraseña con SHA256
    """
    # Hash simple con SHA256 + salt básico
    salt = settings.SECRET_KEY[:16]  # Usar parte del secret key como salt
    return hashlib.sha256((password + salt).encode()).hexdigest()