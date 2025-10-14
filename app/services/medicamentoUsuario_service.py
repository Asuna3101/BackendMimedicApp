"""
Servicio para registrar medicamentos asociados a usuarios
"""
from app.interfaces.medicamento_repository_interface import IMedicamentoRepository
from app.interfaces.medicamento_usuario_repository_interface import IMedicamentoUsuarioRepository
from app.interfaces.medicamento_usuario_service_interface import IMedicamentoUsuarioService
from app.interfaces.unidad_repository_interface import IUnidadRepository


class MedicamentoUsuarioService(IMedicamentoUsuarioService):
    def __init__(
        self,
        med_repo: IMedicamentoRepository,
        unidad_repo: IUnidadRepository,
        medxuser_repo: IMedicamentoUsuarioRepository,
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

    def actualizar_medicamento_usuario(self, id_usuario: int, id_medicamento_usuario: int, data):
        """Actualizar un registro medicamento-usuario.

        Esta función actualiza campos permitidos del registro. No regenera automáticamente
        las tomas asociadas (para eso se debería usar el servicio de tomas o exponer
        métodos adicionales en el repositorio).
        """
        # 1) Validar existencia del registro
        medxuser = self.medxuser_repo.get_by_id(id_medicamento_usuario)
        if not medxuser or medxuser.idUsuario != id_usuario:
            raise ValueError("Registro de medicamento por usuario no encontrado")

        update_data = {}

        # Si cambia el nombre del medicamento, obtener/crear
        if hasattr(data, "nombre") and data.nombre:
            medicamento = self.med_repo.get_or_create_medicamento(data.nombre)
            update_data["idMedicamento"] = medicamento.id

        # Si cambia la unidad
        if hasattr(data, "unidad") and data.unidad:
            unidad = self.unidad_repo.get_or_create_unidad(data.unidad)
            update_data["idUnidad"] = unidad.id

        # Campos directos
        for campo in ("dosis", "frecuencia_horas", "fecha_inicio", "fecha_fin"):
            if hasattr(data, campo):
                update_data[campo] = getattr(data, campo)

        if not update_data:
            return {"message": "No hay cambios"}

        actualizado = self.medxuser_repo.update(id_medicamento_usuario, update_data)
        if not actualizado:
            raise ValueError("No se pudo actualizar el registro")

        return {
            "id": actualizado.id,
            "message": "Medicamento de usuario actualizado correctamente",
        }