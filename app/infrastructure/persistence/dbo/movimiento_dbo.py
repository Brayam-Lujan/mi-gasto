from sqlalchemy import Column, DateTime, Enum, Integer, Numeric, String

from app.config.database import Base
from app.domain.models import TipoMovimiento


# DBO (Data Base Object): representación del movimiento en la capa de persistencia SQLAlchemy
# Es independiente del dominio; solo se usa para mapear a/desde tabla de base de datos
class MovimientoDBO(Base):
    __tablename__ = "movimientos"

    id = Column(Integer, primary_key=True, index=True)
    descripcion = Column(String, nullable=False)
    # Numeric(12,2) almacena valores decimales con precisión compatible con SQLite
    monto = Column(Numeric(12, 2), nullable=False)
    tipo = Column(Enum(TipoMovimiento), nullable=False)
    categoria = Column(String, nullable=False)
    fecha = Column(DateTime, nullable=False)