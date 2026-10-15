from app.contracts.repositories import IMovimientoRepository
from app.domain.exceptions import MovimientoNoEncontradoError


# Caso de uso: elimina un movimiento por su ID
class EliminarMovimiento:
    def __init__(self, repository: IMovimientoRepository):
        self._repository = repository

    def ejecutar(self, movimiento_id: int) -> bool:
        # Verifica que el movimiento exista antes de eliminarlo
        existe = self._repository.obtener_por_id(movimiento_id)
        if existe is None:
            raise MovimientoNoEncontradoError(
                f"No se encontró el movimiento con id {movimiento_id}"
            )
        # Ejecuta la eliminación a través del contrato de repositorio
        return self._repository.eliminar(movimiento_id)