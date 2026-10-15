from decimal import Decimal

from app.domain.models import Movimiento, TipoMovimiento
from app.infrastructure.persistence.dbo.movimiento_dbo import MovimientoDBO


class MovimientoMapper:
    """Mapeador entre entidad de dominio y DBO de persistencia."""

    @staticmethod
    def to_dbo(movimiento: Movimiento) -> MovimientoDBO:
        return MovimientoDBO(
            id=movimiento.id,
            descripcion=movimiento.descripcion,
            monto=movimiento.monto,
            tipo=movimiento.tipo,
            categoria=movimiento.categoria,
            fecha=movimiento.fecha,
        )

    @staticmethod
    def to_domain(dbo: MovimientoDBO) -> Movimiento:
        return Movimiento(
            id=dbo.id,
            descripcion=dbo.descripcion,
            monto=Decimal(str(dbo.monto)),
            tipo=dbo.tipo,
            categoria=dbo.categoria,
            fecha=dbo.fecha,
        )