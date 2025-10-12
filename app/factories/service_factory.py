"""
Factory Pattern para crear servicios y dependencias
Implementa Dependency Injection (DIP)
"""
from sqlalchemy.orm import Session
from app.interfaces.citas_repository_interface import ICitasRepository
from app.interfaces.citas_service_interface import ICitasService
from app.interfaces.user_service_interface import IUserService
from app.interfaces.user_repository_interface import IUserRepository
from app.interfaces.auth_interface import IPasswordHasher, ITokenGenerator
from app.repositories.citas_repository import CitasRepository
from app.services.citas_service import CitasService
from app.services.user_service import UserService
from app.repositories.user_repository import UserRepository
from app.auth.password_hasher import BcryptPasswordHasher
from app.auth.token_generator import JWTTokenGenerator


class ServiceFactory:
    """Factory para crear servicios con sus dependencias inyectadas"""
    
    @staticmethod
    def create_user_repository(db: Session) -> IUserRepository:
        """Crear repositorio de usuarios"""
        return UserRepository(db)
    
    @staticmethod
    def create_citas_repository(db: Session) -> ICitasRepository:
        """Crear repositorio de citas"""
        return CitasRepository(db)
    
    @staticmethod
    def create_citas_service(
            repository: ICitasRepository
        ) -> ICitasService:
        """Crear service de citas"""
        return CitasService(repository)
    
    @staticmethod
    def create_password_hasher() -> IPasswordHasher:
        """Crear hasher de contraseñas"""
        return BcryptPasswordHasher()
    
    @staticmethod
    def create_token_generator() -> ITokenGenerator:
        """Crear generador de tokens"""
        return JWTTokenGenerator()
    
    @staticmethod
    def create_user_service(
        repository: IUserRepository,
        password_hasher: IPasswordHasher
    ) -> IUserService:
        """Crear servicio de usuarios con dependencias inyectadas"""
        return UserService(repository, password_hasher)


    @staticmethod
    def create_auth_service(
        user_service: IUserService,
        token_generator: ITokenGenerator
    ):
        """Crear servicio de autenticación"""
        from app.services.auth_service import AuthService
        return AuthService(user_service, token_generator)