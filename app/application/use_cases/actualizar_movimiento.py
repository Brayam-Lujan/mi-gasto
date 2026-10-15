from app.application.dtos import MovimientoActualizarDTO, MovimientoRespuestaDTO
from app.contracts.repositories import IMovimientoRepository
from app.domain.exceptions import MovimientoNoEncontradoError
from app.domain.models import Movimiento


# Caso de uso: actualiza un movimiento existente (campos opcionales)
class ActualizarMovimiento:
    def __init__(self, repository: IMovimientoRepository):
        self._repository = repository

    def ejecutar(self, movimiento_id: int, dto: MovimientoActualizarDTO) -> MovimientoRespuestaDTO:
        # Verifica que el movimiento exista antes de actualizar
        existente = self._repository.obtener_por_id(movimiento_id)
        if existente is None:
            raise MovimientoNoEncontradoError(
                f"No se encontró el movimiento con id {movimiento_id}"
            )

        # Construye entidad actualizada conservando los valores no proporcionados
        actualizado = Movimiento(
            id=movimiento_id,
            descripcion=dto.descripcion if dto.descripcion is not None else existente.descripcion,
            monto=dto.monto if dto.monto is not None else existente.monto,
            tipo=dto.tipo if dto.tipo is not None else existente.tipo,
            categoria=dto.categoria if dto.categoria is not None else existente.categoria,
            fecha=dto.fecha if dto.fecha is not None else existente.fecha,
        )

        # Guarda los cambios a través del contrato de repositorio
        movimiento_guardado = self._repository.actualizar(actualizado)
        return MovimientoRespuestaDTO(
            id=movimiento_guardado.id,
            descripcion=movimiento_guardado.descripcion,
            monto=movimiento_guardado.monto,
            tipo=movimiento_guardado.tipo,
            categoria=movimiento_guardado.categoria,
            fecha=movimiento_guardado.fecha,
        )