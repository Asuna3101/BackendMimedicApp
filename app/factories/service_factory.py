# app/factories/service_factory.py

"""
Factory Pattern para crear servicios y dependencias
Implementa Dependency Injection (DIP)
"""
from sqlalchemy.orm import Session

# --- Usuarios / Auth ---
from app.interfaces.user_service_interface import IUserService
from app.interfaces.user_repository_interface import IUserRepository
from app.interfaces.auth_interface import IPasswordHasher, ITokenGenerator
from app.repositories.user_repository import UserRepository
from app.services.user_service import UserService
from app.auth.password_hasher import BcryptPasswordHasher
from app.auth.token_generator import JWTTokenGenerator


# --- Medicamentos ---
from app.interfaces.medicamento_repository_interface import IMedicamentoRepository
from app.interfaces.medicamento_service_interface import IMedicamentoService
from app.interfaces.medicamento_usuario_repository_interface import IMedicamentoUsuarioRepository
from app.interfaces.medicamento_usuario_service_interface import IMedicamentoUsuarioService
from app.interfaces.toma_repository_interface import ITomaRepository
from app.interfaces.toma_service_interface import ITomaService
from app.interfaces.unidad_repository_interface import IUnidadRepository
from app.interfaces.unidad_service_interface import IUnidadService
from app.services.medicamentoUsuario_service import MedicamentoUsuarioService
from app.services.medicamento_service import MedicamentoService
from app.services.toma_service import TomaService
from app.services.unidad_service import UnidadService
from app.repositories.unidad_repo import UnidadRepository
from app.repositories.medicamentoUsuario_repo import MedicamentoUsuarioRepository
from app.repositories.toma_repo import TomaRepository
from app.repositories.medicamento_repo import MedicamentoRepository


# --- Appointment Reminders (nuevo flujo) ---
from app.interfaces.appointment_reminder_repository_interface import (
    IAppointmentReminderRepository,
)
from app.interfaces.appointment_reminder_service_interface import (
    IAppointmentReminderService,
)
from app.repositories.appointment_reminder_repo import (
    AppointmentReminderRepository,
)
from app.services.appointment_reminder_service import AppointmentReminderService


class ServiceFactory:
    """Factory para crear servicios con sus dependencias inyectadas"""

    # ---------------- Usuarios / Auth ----------------
    @staticmethod
    def create_user_repository(db: Session) -> IUserRepository:
        return UserRepository(db)

    @staticmethod
    def create_password_hasher() -> IPasswordHasher:
        return BcryptPasswordHasher()


    @staticmethod
    def create_token_generator() -> ITokenGenerator:
        return JWTTokenGenerator()

    @staticmethod
    def create_user_service(
        repository: IUserRepository,
        password_hasher: IPasswordHasher,
    ) -> IUserService:
        return UserService(repository, password_hasher)

    @staticmethod
    def create_auth_service(
        user_repository: IUserRepository,
        token_generator: ITokenGenerator
    ):
        from app.services.auth_service import AuthService
        return AuthService(user_repository, token_generator)

    # ====== MEDICAMENTO ======
    @staticmethod
    def create_medicamento_repository(db: Session) -> IMedicamentoRepository:
        return MedicamentoRepository(db)

    @staticmethod
    def create_medicamento_service(med_repo: IMedicamentoRepository) -> IMedicamentoService:
        return MedicamentoService(med_repo)

    # ====== UNIDAD ======
    @staticmethod
    def create_unidad_repository(db: Session) -> IUnidadRepository:
        return UnidadRepository(db)

    @staticmethod
    def create_unidad_service(unidad_repo: IUnidadRepository) -> IUnidadService:
        return UnidadService(unidad_repo)

    # ====== TOMA ======
    @staticmethod
    def create_toma_repository(db: Session) -> ITomaRepository:
        return TomaRepository(db)

    @staticmethod
    def create_toma_service(toma_repo: ITomaRepository) -> ITomaService:
        return TomaService(toma_repo)


    # ====== MEDICAMENTO x USUARIO ======
    @staticmethod
    def create_medicamento_x_usuario_repository(db: Session) -> IMedicamentoUsuarioRepository:
        return MedicamentoUsuarioRepository(db)

    @staticmethod
    def create_medicamento_x_usuario_service(
        med_repo: IMedicamentoRepository,
        unidad_repo: IUnidadRepository,
        medxuser_repo: IMedicamentoUsuarioRepository,
    ) -> IMedicamentoUsuarioService:
        return MedicamentoUsuarioService(med_repo, unidad_repo, medxuser_repo)

    # --------- Appointment Reminders (nuevo) ----------
    @staticmethod
    def create_appointment_reminder_repository(db: Session) -> IAppointmentReminderRepository:
        return AppointmentReminderRepository(db)

    @staticmethod
    def create_appointment_reminder_service(db: Session) -> IAppointmentReminderService:
        return AppointmentReminderService(db)