from fastapi import APIRouter, Depends
from app.api.v1.endpoints.dependencies import get_current_user
from app.schemas.user import UserProfile

router = APIRouter()

@router.get("/me", response_model=UserProfile)
def get_my_profile(user=Depends(get_current_user)):
    """Retorna el perfil del usuario autenticado."""
    return user