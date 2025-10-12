"""
Servicio para gestión de tomas 
"""
from app.interfaces.toma_repository_interface import ITomaRepository
from app.interfaces.toma_service_interface import ITomaService


class TomaService(ITomaService):
    def __init__(self, toma_repo: ITomaRepository):
        self.toma_repo = toma_repo

    def marcar_toma(self, toma_id: int, tomado: bool):
        toma = self.toma_repo.update_tomado(toma_id, tomado)
        if not toma:
            raise ValueError("Toma no encontrada")

        # Si todas las tomas de ese medxuser están en True, limpiar
        pendientes = self.toma_repo.count_pendientes_by_medxuser(toma.idMedxUser)
        if pendientes == 0:
            self.toma_repo.delete_all_by_medxuser(toma.idMedxUser)

        return toma
