from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from enum import Enum


# Tipo de movimiento financiero: ingreso o gasto
class TipoMovimiento(str, Enum):
    INGRESO = "INGRESO"
    GASTO = "GASTO"


# Entidad de dominio: representa un movimiento financiero (ingreso o gasto)
# Es independiente de frameworks (FastAPI, SQLAlchemy) y de persistencia
@dataclass
class Movimiento:
    id: int | None          # Identificador único (None al crear, se asigna al guardar)
    descripcion: str        # Descripción del movimiento
    monto: Decimal          # Monto monetario (usa Decimal para precisión)
    tipo: TipoMovimiento    # INGRESO o GASTO
    categoria: str          # Categoría del movimiento (ej: Trabajo, Alimentación)
    fecha: datetime         # Fecha y hora del movimiento