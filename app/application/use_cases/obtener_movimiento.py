from app.application.dtos import MovimientoRespuestaDTO
from app.contracts.repositories import IMovimientoRepository
from app.domain.exceptions import MovimientoNoEncontradoError


class ObtenerMovimiento:
    def __init__(self, repository: IMovimientoRepository):
        self._repository = repository

    def ejecutar(self, movimiento_id: int) -> MovimientoRespuestaDTO:
        movimiento = self._repository.obtener_por_id(movimiento_id)
        if movimiento is None:
            raise MovimientoNoEncontradoError(
                f"No se encontró el movimiento con id {movimiento_id}"
            )
        return MovimientoRespuestaDTO(
            id=movimiento.id,
            descripcion=movimiento.descripcion,
            monto=movimiento.monto,
            tipo=movimiento.tipo,
            categoria=movimiento.categoria,
            fecha=movimiento.fecha,
        )