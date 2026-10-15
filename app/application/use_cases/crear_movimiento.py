from app.application.dtos import MovimientoCrearDTO, MovimientoRespuestaDTO
from app.contracts.repositories import IMovimientoRepository
from app.domain.models import Movimiento


class CrearMovimiento:
    def __init__(self, repository: IMovimientoRepository):
        self._repository = repository

    def ejecutar(self, dto: MovimientoCrearDTO) -> MovimientoRespuestaDTO:
        movimiento = Movimiento(
            id=None,
            descripcion=dto.descripcion,
            monto=dto.monto,
            tipo=dto.tipo,
            categoria=dto.categoria,
            fecha=dto.fecha,
        )
        movimiento_guardado = self._repository.guardar(movimiento)
        return MovimientoRespuestaDTO(
            id=movimiento_guardado.id,
            descripcion=movimiento_guardado.descripcion,
            monto=movimiento_guardado.monto,
            tipo=movimiento_guardado.tipo,
            categoria=movimiento_guardado.categoria,
            fecha=movimiento_guardado.fecha,
        )