"""
Controlador para Citas usando ServiceFactory (DIP)
"""
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.factories.service_factory import ServiceFactory


class CitasController:
    def __init__(self, db: Session):
        # Inyección de dependencias con ServiceFactory
        citas_repo = ServiceFactory.create_citas_repository(db)

        self.service = ServiceFactory.create_citas_service(repository=citas_repo)
            
    def obtener_citas_usuario(self, id_usuario: int):
        return self.service.obtener_citas_por_usuario(id_usuario)