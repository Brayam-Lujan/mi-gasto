from sqlalchemy import Column, DateTime, Enum, Integer, Numeric, String

from app.config.database import Base
from app.domain.models import TipoMovimiento


class MovimientoDBO(Base):
    """Data Base Object: representación del movimiento en la capa de persistencia."""

    __tablename__ = "movimientos"

    id = Column(Integer, primary_key=True, index=True)
    descripcion = Column(String, nullable=False)
    # Numeric permite almacenar valores decimales de forma compatible con SQLite
    # y se lee de nuevo como Decimal mediante el mapeador.
    monto = Column(Numeric(12, 2), nullable=False)
    tipo = Column(Enum(TipoMovimiento), nullable=False)
    categoria = Column(String, nullable=False)
    fecha = Column(DateTime, nullable=False)