"""
Recrea la tabla de usuarios y crea un usuario de prueba (bcrypt).
"""
import os, sys
from sqlalchemy import text
from sqlalchemy.orm import sessionmaker

# Agregar el directorio del proyecto al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.database import engine
from app.models.base import Base
from app.models.user import User
from app.auth.password_hasher import BcryptPasswordHasher  # ⬅️ usa bcrypt

def recreate_users_table():
    try:
        # 1) Dropear tabla usuarios (misma DB que usa la app)
        with engine.connect() as conn:
            conn.execute(text("DROP TABLE IF EXISTS usuarios CASCADE"))
            conn.commit()
            print("Tabla 'usuarios' eliminada")

        # 2) Crear tablas nuevamente (metadata completo)
        Base.metadata.create_all(bind=engine)
        print("Tabla 'usuarios' recreada")

        # 3) Crear usuario de prueba
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        db = SessionLocal()
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
        print(f"Error: {e}")
    finally:
        try:
            db.close()
        except:
            pass

if __name__ == "__main__":
    recreate_users_table()
