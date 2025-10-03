"""
Script para crear un usuario de prueba en la base de datos
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import sys
import os

# Agregar el directorio del proyecto al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.config import settings
from app.models.user import User
from app.core.database import get_db, engine
from app.auth.password_hasher import SimplePasswordHasher

# Crear tablas si no existen
from app.models import base
base.Base.metadata.create_all(bind=engine)

def create_test_user():
    """Crear usuario de prueba"""
    # Crear sesión de base de datos
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    
    # Verificar si ya existe el usuario
    existing_user = db.query(User).filter(User.correo == "test@example.com").first()
    if existing_user:
        print("El usuario test@example.com ya existe")
        db.close()
        return
    
    # Crear hasher de contraseñas
    password_hasher = SimplePasswordHasher()
    
    # Crear usuario de prueba
    test_user = User(
        correo="test@example.com",
        nombre="Usuario de Prueba",
        fecha_nacimiento=None,
        celular="1234567890",
        hashed_password=password_hasher.hash_password("test123"),
        is_active=True
    )
    
    try:
        db.add(test_user)
        db.commit()
        print("Usuario de prueba creado exitosamente:")
        print(f"- Correo: test@example.com")
        print(f"- Contraseña: test123")
        print(f"- Nombre: Usuario de Prueba")
    except Exception as e:
        db.rollback()
        print(f"Error al crear usuario: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    create_test_user()