from typing import List

from app.application.dtos import MovimientoRespuestaDTO
from app.contracts.repositories import IMovimientoRepository


# Caso de uso: lista todos los movimientos almacenados
class ListarMovimientos:
    def __init__(self, repository: IMovimientoRepository):
        self._repository = repository

    def ejecutar(self) -> List[MovimientoRespuestaDTO]:
        # Obtiene todos los movimientos a través del contrato de repositorio
        movimientos = self._repository.listar()
        # Convierte cada entidad de dominio en un DTO de respuesta
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