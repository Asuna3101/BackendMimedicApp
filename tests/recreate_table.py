"""
Script para recrear la tabla de usuarios con auto-increment
"""
from sqlalchemy import create_engine, text
import sys
import os

# Agregar el directorio del proyecto al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.config import settings
from app.models.user import User
from app.core.database import engine
from app.auth.password_hasher import SimplePasswordHasher

def recreate_users_table():
    """Recrear tabla de usuarios"""
    
    try:
        # Eliminar tabla existente
        with engine.connect() as conn:
            conn.execute(text("DROP TABLE IF EXISTS usuarios CASCADE"))
            conn.commit()
            print("Tabla usuarios eliminada")
        
        # Crear tablas nuevamente
        from app.models import base
        base.Base.metadata.create_all(bind=engine)
        print("Tabla usuarios recreada con auto-increment")
        
        # Crear usuario de prueba
        from sqlalchemy.orm import sessionmaker
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        db = SessionLocal()
        
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
        
        db.add(test_user)
        db.commit()
        print("Usuario de prueba creado exitosamente:")
        print(f"- Correo: test@example.com")
        print(f"- Contraseña: test123")
        print(f"- Nombre: Usuario de Prueba")
        
        db.close()
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    recreate_users_table()