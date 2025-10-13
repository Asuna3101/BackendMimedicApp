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

# --- Appointment Reminders (nuevo flujo) ---
from app.interfaces.appointment_reminder_repository_interface import (
    IAppointmentReminderRepository,
)
from app.interfaces.appointment_reminder_service_interface import (
    IAppointmentReminderService,
)
from app.repositories.appointment_reminder_repository import (
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
        token_generator: ITokenGenerator,
        password_hasher: IPasswordHasher,
    ):
        from app.services.auth_service import AuthService
        return AuthService(user_repository, token_generator, password_hasher)

    # --------- Appointment Reminders (nuevo) ----------
    @staticmethod
    def create_appointment_reminder_repository(db: Session) -> IAppointmentReminderRepository:
        return AppointmentReminderRepository(db)

    @staticmethod
    def create_appointment_reminder_service(
        repository: IAppointmentReminderRepository,
    ) -> IAppointmentReminderService:
        return AppointmentReminderService(repository)
