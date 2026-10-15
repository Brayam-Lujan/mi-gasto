from typing import List

from app.application.dtos import MovimientoRespuestaDTO
from app.contracts.repositories import IMovimientoRepository


class ListarMovimientos:
    def __init__(self, repository: IMovimientoRepository):
        self._repository = repository

    def ejecutar(self) -> List[MovimientoRespuestaDTO]:
        movimientos = self._repository.listar()
        return [
            MovimientoRespuestaDTO(
                id=m.id,
                descripcion=m.descripcion,
                monto=m.monto,
                tipo=m.tipo,
                categoria=m.categoria,
                fecha=m.fecha,
            )
            for m in movimientos
        ]