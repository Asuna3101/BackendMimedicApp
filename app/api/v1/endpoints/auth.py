"""
Endpoint de autenticación (login / register)
"""
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.factories.service_factory import ServiceFactory
from app.controllers.user_controller import UserController
from app.services.auth_service import AuthService

from app.schemas.user import Token, UserLogin, UserCreate

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=Token)
def login(user_login: UserLogin, db: Session = Depends(get_db)):
    """
    Autentica y devuelve un access token.
    Body esperado (front):
      { "correo": "...", "password": "..." }
    """
    # Construir AuthService con dependencias reales
    user_repo = ServiceFactory.create_user_repository(db)
    pwd_hasher = ServiceFactory.create_password_hasher()
    token_gen  = ServiceFactory.create_token_generator()
    auth = AuthService(user_repo, token_gen, pwd_hasher)

    # Genera token o levanta 401 si credenciales inválidas
    data = auth.authenticate_and_create_token(
        correo=user_login.correo,
        password=user_login.password,
    )
    # Token schema debe reflejar lo que devuelves aquí.
    # Si tu Token solo tiene access_token y token_type, retorna solo esas claves:
    # return {"access_token": data["access_token"], "token_type": data["token_type"]}
    return data


@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(user_create: UserCreate, db: Session = Depends(get_db)):
    """
    Registra un nuevo usuario.
    Body esperado:
      {
        "correo": "...",
        "password": "...",
        "nombre": "...",
        "fecha_nacimiento": "YYYY-MM-DD",
        "celular": "..."
      }
    """
    controller = UserController(db)

    # Parsear fecha de nacimiento
    try:
        fecha = datetime.fromisoformat(user_create.fecha_nacimiento).date()
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="fecha_nacimiento debe ser YYYY-MM-DD",
        )

    try:
        user = controller.register_user(
            correo=user_create.correo,
            password=user_create.password,
            nombre=user_create.nombre,
            fecha_nacimiento=fecha,
            celular=user_create.celular,
        )
        return {"id": user.id, "correo": user.correo}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
