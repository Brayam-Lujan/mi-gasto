from app.application.dtos import MovimientoActualizarDTO, MovimientoRespuestaDTO
from app.contracts.repositories import IMovimientoRepository
from app.domain.exceptions import MovimientoNoEncontradoError
from app.domain.models import Movimiento


class ActualizarMovimiento:
    def __init__(self, repository: IMovimientoRepository):
        self._repository = repository

    def ejecutar(self, movimiento_id: int, dto: MovimientoActualizarDTO) -> MovimientoRespuestaDTO:
        existente = self._repository.obtener_por_id(movimiento_id)
        if existente is None:
            raise MovimientoNoEncontradoError(
                f"No se encontró el movimiento con id {movimiento_id}"
            )

        actualizado = Movimiento(
            id=movimiento_id,
            descripcion=dto.descripcion if dto.descripcion is not None else existente.descripcion,
            monto=dto.monto if dto.monto is not None else existente.monto,
            tipo=dto.tipo if dto.tipo is not None else existente.tipo,
            categoria=dto.categoria if dto.categoria is not None else existente.categoria,
            fecha=dto.fecha if dto.fecha is not None else existente.fecha,
        )

        movimiento_guardado = self._repository.actualizar(actualizado)
        return MovimientoRespuestaDTO(
            id=movimiento_guardado.id,
            descripcion=movimiento_guardado.descripcion,
            monto=movimiento_guardado.monto,
            tipo=movimiento_guardado.tipo,
            categoria=movimiento_guardado.categoria,
            fecha=movimiento_guardado.fecha,
        )