"""
Servicio para registrar medicamentos asociados a usuarios
"""
from app.models.medicamento import Medicamento
from app.models.medicamentoUsuario import MedicamentoUsuario
from app.models.unidad import Unidad
from app.repositories.medicamento_repo import MedicamentoRepository
from app.repositories.unidad_repo import UnidadRepository
from app.repositories.medicamentoUsuario_repo import MedicamentoUsuarioRepository


class MedicamentoUsuarioService:
    def __init__(
        self,
        med_repo: MedicamentoRepository,
        unidad_repo: UnidadRepository,
        medxuser_repo: MedicamentoUsuarioRepository,
    ):
        self.med_repo = med_repo
        self.unidad_repo = unidad_repo
        self.medxuser_repo = medxuser_repo

    def registrar_medicamento_usuario(self, id_usuario: int, data):
        # 1) Catálogos
        medicamento = self.med_repo.get_or_create_medicamento(data.nombre)
        unidad = self.unidad_repo.get_or_create_unidad(data.unidad)

        # 2) Asociación user-medicamento
        medxuser_data = {
            "idUsuario": id_usuario,
            "idMedicamento": medicamento.id,
            "idUnidad": unidad.id,
            "dosis": data.dosis,
            "frecuencia_horas": data.frecuencia_horas,
            "fecha_inicio": data.fecha_inicio,
            "fecha_fin": data.fecha_fin,
        }
        medxuser = self.medxuser_repo.create(medxuser_data)

        # 3) Generar tomas
        self.medxuser_repo.generate_tomas(medxuser)

        return {
            "id": medicamento.id,
            "nombre": medicamento.nombre,
            "message": "Medicamento guardado correctamente",
        }

    def obtener_medicamentos_por_usuario(self, id_usuario: int):
        rows = self.medxuser_repo.get_by_usuario(id_usuario)
        result = [
            {
                "id": mxu.id,
                "nombre": med.nombre,
                "dosis": mxu.dosis,
                "unidad": un.nombre,
                "frecuenciaHoras": mxu.frecuencia_horas,
                "fechaInicio": mxu.fecha_inicio,
                "fechaFin": mxu.fecha_fin,
            }
            for mxu, med, un in rows
        ]
        return result