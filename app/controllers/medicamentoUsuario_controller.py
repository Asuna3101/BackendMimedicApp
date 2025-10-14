"""
Controlador para MedicamentoXUsuario usando ServiceFactory (DIP)
"""
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.factories.service_factory import ServiceFactory


class MedicamentoUsuarioController:
    def __init__(self, db: Session):
        # Inyección de dependencias con ServiceFactory
        med_repo = ServiceFactory.create_medicamento_repository(db)
        unidad_repo = ServiceFactory.create_unidad_repository(db)
        medxuser_repo = ServiceFactory.create_medicamento_x_usuario_repository(db)

        self.service = ServiceFactory.create_medicamento_x_usuario_service(
            med_repo, unidad_repo, medxuser_repo
        )

    def registrar_medicamento_usuario(self, id_usuario: int, data):
        try:
            return self.service.registrar_medicamento_usuario(id_usuario, data)
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e),
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al registrar medicamento para usuario: {str(e)}",
            )
            
    def obtener_medicamentos_usuario(self, id_usuario: int):
        return self.service.obtener_medicamentos_por_usuario(id_usuario)

    def actualizar_medicamento_usuario(self, id_usuario: int, id_medicamento_usuario: int, data):
        try:
            return self.service.actualizar_medicamento_usuario(id_usuario, id_medicamento_usuario, data)
        except ValueError as e:
            # Usar 404 o 400 según el mensaje
            msg = str(e)
            code = status.HTTP_404_NOT_FOUND if "no encontrado" in msg.lower() else status.HTTP_400_BAD_REQUEST
            raise HTTPException(status_code=code, detail=msg)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al actualizar medicamento de usuario: {str(e)}",
            )