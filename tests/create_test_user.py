"""
Script para crear un usuario de prueba en la base de datos
"""
import os, sys
from sqlalchemy.orm import sessionmaker

# Agregar el directorio del proyecto al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.database import engine
from app.models.base import Base
import app.models  # ⬅️ registra TODOS los modelos en el metadata
from app.models.user import User
from app.auth.password_hasher import BcryptPasswordHasher  # ⬅️ usa bcrypt

# Crear tablas si no existen (solo para dev; en prod usa Alembic)
Base.metadata.create_all(bind=engine)

def create_test_user():
    """Crear usuario de prueba con bcrypt"""
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    try:
        existing = db.query(User).filter(User.correo == "test@example.com").first()
        if existing:
            print("El usuario test@example.com ya existe")
            return

        hasher = BcryptPasswordHasher()
        test_user = User(
            correo="test@example.com",
            nombre="Usuario de Prueba",
            fecha_nacimiento=None,
            celular="1234567890",
            hashed_password=hasher.hash_password("test123"),
            is_active=True,
        )
        db.add(test_user)
        db.commit()
        print("Usuario de prueba creado:")
        print("- Correo: test@example.com")
        print("- Contraseña: test123")
    except Exception as e:
        db.rollback()
        print(f"Error al crear usuario: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    create_test_user()
