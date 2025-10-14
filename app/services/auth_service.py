"""
Servicio de Autenticación - SRP (Single Responsibility Principle)
Solo se encarga de la lógica de autenticación y tokens
"""
from datetime import timedelta
from typing import Optional

from fastapi import HTTPException, status

from app.interfaces.user_service_interface import IUserService
from app.models.user import User
from app.interfaces.user_repository_interface import IUserRepository
from app.interfaces.auth_interface import ITokenGenerator, IPasswordHasher


class AuthService:
    """Servicio dedicado a autenticación (verificación y emisión de tokens)"""

    def __init__(self, user_service: IUserService, token_generator: ITokenGenerator):
        self.user_service = user_service
        self.token_generator = token_generator
    
    # def __init__(
    #     self,
    #     user_repo: IUserRepository,
    #     token_generator: ITokenGenerator,
        # password_hasher: IPasswordHasher,
    # ):
    #     self.user_repo = user_repo
    #     self.token_generator = token_generator
        # self.password_hasher = password_hasher

#     def authenticate_and_create_token(
#         self,
#         correo: str,
#         password: str,
#         expires_delta: Optional[timedelta] = None,
#     ) -> dict:
#         """
#         Autentica usuario por correo + password (bcrypt) y genera access token.
#         Lanza 401 si las credenciales son inválidas.
#         """
#         user: Optional[User] = self.user_repo.get_by_email(correo)
#         if not user or not user.is_active:
#             raise HTTPException(
#                 status_code=status.HTTP_401_UNAUTHORIZED,
#                 detail="Credenciales inválidas",
#             )
#
#         # Verifica contra hashed_password (bcrypt)
#         if not self.password_hasher.verify_password(password, user.hashed_password):
#             raise HTTPException(
#                 status_code=status.HTTP_401_UNAUTHORIZED,
#                 detail="Credenciales inválidas",
#             )
#
#         # SUBJECT = user.id (no correo)
#         access_token = self.token_generator.create_access_token(
#             subject=user.id,               # <-- SOLO el id
#             expires_delta=expires_delta,
#         )

    def authenticate_and_create_token(
        self,
        correo: str,
        password: str,
        expires_delta: Optional[timedelta] = None
    ) -> Optional[dict]:
        """
        Autentica usuario y genera token
        Retorna None si las credenciales son inválidas
        """
        # Autenticar usuario
        user = self.user_service.authenticate_user(correo, password)
        if not user:
            return None

        # Generar token
        access_token = self.token_generator.create_access_token(
            subject=user.correo,
            expires_delta=expires_delta
        )

        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": user
        }

        # # Devuelve payload mínimo (no el ORM completo)
        # return {
        #     "access_token": access_token,
        #     "token_type": "bearer",
        #     "user": {
        #         "id": user.id,
        #         "correo": user.correo,
        #         "nombre": user.nombre,
        #         "is_active": user.is_active,
        #         "is_superuser": user.is_superuser,
        #     },
        # }

#     def verify_token(self, token: str) -> Optional[dict]:
#         """
#         Verificar token y devolver el payload (o None si inválido/expirado)
#         """
#         payload = self.token_generator.decode_token(token)
#         return payload or None

    def verify_token(self, token: str) -> Optional[str]:
        """
        Verificar token y extraer username
        """
        payload = self.token_generator.decode_token(token)
        if not payload:
            return None

        return payload.get("sub")

#     def get_user_from_token(self, token: str) -> Optional[User]:
#         """
#         Cargar el usuario a partir del token (usa sub = user.id)
#         """
#         payload = self.verify_token(token)
#         if not payload:
#             return None
#         user_id = payload.get("sub")
#         if not user_id:
#             return None
#         # id almacenado como string -> convierte a int si aplica
#         try:
#             user_id = int(user_id)
#         except (TypeError, ValueError):
#             return None
#         return self.user_repo.get_by_id(user_id)

#     def refresh_token(self, user: User, expires_delta: Optional[timedelta] = None) -> str:
#         return self.token_generator.create_access_token(
#             subject=user.id,           # <-- idem
#             expires_delta=expires_delta,
#         )

    def refresh_token(self, user: User, expires_delta: Optional[timedelta] = None) -> str:
        return self.token_generator.create_access_token(
            subject=user.id,           # <-- idem
            expires_delta=expires_delta,
        )

    def refresh_token(self, user: User, expires_delta: Optional[timedelta] = None) -> str:
        """
        Generar nuevo token para usuario existente
        """
        return self.token_generator.create_access_token(
            subject=user.correo,
            expires_delta=expires_delta
        )

    def get_user_from_token(self, token: str) -> Optional[User]:
        email = self.verify_token(token)
        if not email:
            return None

        user = self.user_service.get_user_by_email(email)
        return user
