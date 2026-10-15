from decimal import Decimal

from app.domain.models import Movimiento, TipoMovimiento
from app.infrastructure.persistence.dbo.movimiento_dbo import MovimientoDBO


# Mapeador entre entidad de dominio y DBO de persistencia (y viceversa)
# Permite que el dominio no conozca SQLAlchemy ni la estructura de la tabla
class MovimientoMapper:

    @staticmethod
    def to_dbo(movimiento: Movimiento) -> MovimientoDBO:
        # Convierte entidad de dominio a DBO para guardar en base de datos
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
        # Convierte DBO leído de la base de datos a entidad de dominio
        return Movimiento(
            id=dbo.id,
            descripcion=dbo.descripcion,
            monto=Decimal(str(dbo.monto)),  # Numeric se lee como Decimal para precisión monetaria
            tipo=dbo.tipo,
            categoria=dbo.categoria,
            fecha=dbo.fecha,
        )