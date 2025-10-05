"""
Controlador de Login - Solo manejo de autenticación
"""
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.factories.service_factory import ServiceFactory


class UserController:
    """Controlador simplificado solo para login"""
    
    def __init__(self, db: Session):
        # Crear servicios necesarios para autenticación
        repository = ServiceFactory.create_user_repository(db)
        password_hasher = ServiceFactory.create_password_hasher()
        self.service = ServiceFactory.create_user_service(repository, password_hasher)
    
    def authenticate_user(self, correo: str, password: str) -> dict:
        """Autenticar usuario y generar token"""
        try:
            # Crear servicio de autenticación
            token_generator = ServiceFactory.create_token_generator()
            auth_service = ServiceFactory().create_auth_service(self.service, token_generator)
            
            # Autenticar y crear token
            auth_result = auth_service.authenticate_and_create_token(correo, password)
            
            if not auth_result:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Credenciales incorrectas",
                    headers={"WWW-Authenticate": "Bearer"}
                )
            
            return {
                "access_token": auth_result["access_token"],
                "token_type": auth_result["token_type"]
            }
            
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error interno del servidor"
            )

    def register_user(self, correo: str, password: str, nombre: str, fecha_nacimiento, celular: str):
        """Registrar usuario delegando en el servicio de usuarios"""
        try:
            created = self.service.register_user(
                correo=correo,
                password=password,
                nombre=nombre,
                fecha_nacimiento=fecha_nacimiento,
                celular=celular,
            )
            return created
        except ValueError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))