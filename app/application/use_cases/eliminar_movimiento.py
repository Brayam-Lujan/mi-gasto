from app.contracts.repositories import IMovimientoRepository
from app.domain.exceptions import MovimientoNoEncontradoError


class EliminarMovimiento:
    def __init__(self, repository: IMovimientoRepository):
        self._repository = repository

    def ejecutar(self, movimiento_id: int) -> bool:
        existe = self._repository.obtener_por_id(movimiento_id)
        if existe is None:
            raise MovimientoNoEncontradoError(
                f"No se encontró el movimiento con id {movimiento_id}"
            )
        return self._repository.eliminar(movimiento_id)