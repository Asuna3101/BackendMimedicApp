"""
Controlador de Login - Solo manejo de autenticación
"""
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.factories.service_factory import ServiceFactory
from app.services.auth_service import AuthService


class UserController:
    """Controlador simplificado solo para login"""

    def __init__(self, db: Session):
        # Dependencias compartidas
        self.user_repo = ServiceFactory.create_user_repository(db)
        self.password_hasher = ServiceFactory.create_password_hasher()
        self.token_generator = ServiceFactory.create_token_generator()

        # Servicios
        self.user_service = ServiceFactory.create_user_service(
            self.user_repo, self.password_hasher
        )

        # AuthService con firma NUEVA: (user_repo, token_gen, password_hasher)
        self.auth_service = AuthService(
            self.user_repo, self.token_generator, self.password_hasher
        )

    def authenticate_user(self, correo: str, password: str) -> dict:
        """Autenticar usuario y generar token"""
        try:
            auth_result = self.auth_service.authenticate_and_create_token(
                correo=correo,
                password=password,
            )
            # Si tu schema Token solo admite access_token y token_type:
            return {
                "access_token": auth_result["access_token"],
                "token_type": auth_result["token_type"],
            }
        except HTTPException:
            # Propaga 401 u otros que lance AuthService
            raise
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
            )
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error interno del servidor",
            )

    def register_user(
        self,
        correo: str,
        password: str,
        nombre: str,
        fecha_nacimiento,
        celular: str,
    ):
        """Registrar usuario delegando en el servicio de usuarios"""
        try:
            created = self.user_service.register_user(
                correo=correo,
                password=password,
                nombre=nombre,
                fecha_nacimiento=fecha_nacimiento,
                celular=celular,
            )
            return created
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
            )

    def get_current_user_from_token(self, token: str):
        """Obtiene el usuario autenticado a partir del token."""
        user = self.auth_service.get_user_from_token(token)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido o usuario no encontrado",
            )
        return user
