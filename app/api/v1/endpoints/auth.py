"""
Endpoint de login simplificado
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.controllers.user_controller import UserController
from app.schemas.user import Token, UserLogin
from app.schemas.user import UserCreate
from fastapi import HTTPException, status
from datetime import datetime

router = APIRouter()


@router.post("/login", response_model=Token)
def login(
    user_login: UserLogin,
    db: Session = Depends(get_db)
):
    """Endpoint único para login de usuario"""
    controller = UserController(db)
    
    # Autenticar usuario usando el controlador
    user_data = controller.authenticate_user(user_login.correo, user_login.password)
    
    return user_data



@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(
    user_create: UserCreate,
    db: Session = Depends(get_db)
):
    """Registrar un nuevo usuario"""
    controller = UserController(db)

    # Parsear fecha de nacimiento
    try:
        fecha = datetime.fromisoformat(user_create.fecha_nacimiento).date()
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="fecha_nacimiento debe ser YYYY-MM-DD")

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
    
    def get_current_user_from_token(self, token: str):
        """Obtiene el usuario autenticado a partir del token."""
        user = self.auth_service.get_user_from_token(token)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido o usuario no encontrado"
            )
        return user