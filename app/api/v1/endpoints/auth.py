"""
Endpoint de login simplificado
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.controllers.user_controller import UserController
from app.schemas.user import Token, UserLogin

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