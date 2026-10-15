from app.application.dtos import MovimientoRespuestaDTO
from app.contracts.repositories import IMovimientoRepository
from app.domain.exceptions import MovimientoNoEncontradoError


# Caso de uso: obtiene un movimiento por su ID
class ObtenerMovimiento:
    def __init__(self, repository: IMovimientoRepository):
        self._repository = repository

    def ejecutar(self, movimiento_id: int) -> MovimientoRespuestaDTO:
        # Busca el movimiento a través del contrato de repositorio
        movimiento = self._repository.obtener_por_id(movimiento_id)
        if movimiento is None:
            raise MovimientoNoEncontradoError(
                f"No se encontró el movimiento con id {movimiento_id}"
            )
        # Retorna DTO de respuesta con los datos encontrados
        return MovimientoRespuestaDTO(
            id=movimiento.id,
            descripcion=movimiento.descripcion,
            monto=movimiento.monto,
            tipo=movimiento.tipo,
            categoria=movimiento.categoria,
            fecha=movimiento.fecha,
        )