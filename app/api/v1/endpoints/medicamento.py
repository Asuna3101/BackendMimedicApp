from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.controllers.medicamento_controller import MedicamentoController

router = APIRouter()

@router.get("/")
def listar_medicamentos(db: Session = Depends(get_db)):
    controller = MedicamentoController(db)
    return controller.listar_todos()
