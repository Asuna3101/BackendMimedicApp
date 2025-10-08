"""
Factory Pattern para crear servicios y dependencias
Implementa Dependency Injection (DIP)
"""
from sqlalchemy.orm import Session
from app.interfaces.user_service_interface import IUserService
from app.interfaces.user_repository_interface import IUserRepository
from app.interfaces.auth_interface import IPasswordHasher, ITokenGenerator
from app.services.user_service import UserService
from app.repositories.user_repository import UserRepository
from app.auth.password_hasher import BcryptPasswordHasher
from app.auth.token_generator import JWTTokenGenerator

from app.repositories.medicamento_repo import MedicamentoRepository
from app.repositories.unidad_repo import UnidadRepository
from app.repositories.medicamentoUsuario_repo import MedicamentoUsuarioRepository
from app.repositories.toma_repo import TomaRepository

from app.services.medicamentoUsuario_service import MedicamentoUsuarioService
from app.services.medicamento_service import MedicamentoService
from app.services.unidad_service import UnidadService
from app.services.toma_service import TomaService


class ServiceFactory:
    """Factory para crear servicios con sus dependencias inyectadas"""
    
    @staticmethod
    def create_user_repository(db: Session) -> IUserRepository:
        """Crear repositorio de usuarios"""
        return UserRepository(db)
    
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
    
    # ====== MEDICAMENTO ======
    @staticmethod
    def create_medicamento_repository(db: Session) -> MedicamentoRepository:
        return MedicamentoRepository(db)

    @staticmethod
    def create_unidad_repository(db: Session) -> UnidadRepository:
        return UnidadRepository(db)

    @staticmethod
    def create_medicamento_service(med_repo: MedicamentoRepository) -> MedicamentoService:
        return MedicamentoService(med_repo)

    @staticmethod
    def create_unidad_service(unidad_repo: UnidadRepository) -> UnidadService:
        return UnidadService(unidad_repo)

    # ====== NUEVOS: MEDICAMENTO x USUARIO ======
    @staticmethod
    def create_medicamento_x_usuario_repository(db: Session) -> MedicamentoUsuarioRepository:
        return MedicamentoUsuarioRepository(db)

    @staticmethod
    def create_medicamento_x_usuario_service(
        med_repo: MedicamentoRepository,
        unidad_repo: UnidadRepository,
        medxuser_repo: MedicamentoUsuarioRepository,
    ) -> MedicamentoUsuarioService:
        return MedicamentoUsuarioService(med_repo, unidad_repo, medxuser_repo)

    # ====== MEDICAMENTOS ======
    
    @staticmethod
    def create_medicamento_repository(db):
        return MedicamentoRepository(db)

    @staticmethod
    def create_medicamento_service(med_repo):
        return MedicamentoService(med_repo)
    
    # ====== UNIDADES ======
    
    @staticmethod
    def create_unidad_repository(db):
        return UnidadRepository(db)

    @staticmethod
    def create_unidad_service(unidad_repo):
        return UnidadService(unidad_repo)

    # ====== TOMAS ======
    @staticmethod
    def create_toma_repository(db: Session) -> TomaRepository:
        return TomaRepository(db)

    @staticmethod
    def create_toma_service(toma_repo: TomaRepository) -> TomaService:
        return TomaService(toma_repo)