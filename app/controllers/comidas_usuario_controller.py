from app.factories.service_factory import ServiceFactory
from sqlalchemy.orm import Session
from fastapi import HTTPException, status


class ComidaUsuarioController:
    def __init__(self, db: Session):
        cu_repo = ServiceFactory.create_comida_usuario_repository(db)
        self.service = ServiceFactory.create_comida_usuario_service(cu_repo)

    def create_for_user(self, comida_id: int, usuario_id: int, categoria_id: int | None = None):
        try:
            return self.service.create_for_user(comida_id, usuario_id, categoria_id)
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    def list_for_user(self, usuario_id: int):
        try:
            return self.service.list_for_user(usuario_id)
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    def delete(self, id: int):
        try:
            ok = self.service.delete(id)
            if not ok:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Registro no encontrado")
            return {"deleted": True}
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
