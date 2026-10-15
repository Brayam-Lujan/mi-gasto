from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from enum import Enum


class TipoMovimiento(str, Enum):
    INGRESO = "INGRESO"
    GASTO = "GASTO"


@dataclass
class Movimiento:
    id: int | None
    descripcion: str
    monto: Decimal
    tipo: TipoMovimiento
    categoria: str
    fecha: datetime