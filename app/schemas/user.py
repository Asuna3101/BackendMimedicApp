"""
Esquemas simplificados solo para Login
"""
from pydantic import BaseModel, EmailStr


# Esquemas para autenticación - Solo lo necesario para login
class Token(BaseModel):
    access_token: str
    token_type: str


class UserLogin(BaseModel):
    correo: EmailStr
    password: str


class UserCreate(BaseModel):
    correo: EmailStr
    password: str
    nombre: str
    fecha_nacimiento: str  # ISO date (YYYY-MM-DD)
    celular: str