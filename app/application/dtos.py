from datetime import datetime
from decimal import Decimal

from app.domain.models import TipoMovimiento


# DTO (objeto de transferencia de datos) para crear un nuevo movimiento
class MovimientoCrearDTO:
    def __init__(
        self,
        descripcion: str,
        monto: Decimal,
        tipo: TipoMovimiento,
        categoria: str,
        fecha: datetime,
    ):
        self.descripcion = descripcion
        self.monto = monto
        self.tipo = tipo
        self.categoria = categoria
        self.fecha = fecha


# DTO para actualizar un movimiento existente (todos los campos opcionales)
class MovimientoActualizarDTO:
    def __init__(
        self,
        descripcion: str | None = None,
        monto: Decimal | None = None,
        tipo: TipoMovimiento | None = None,
        categoria: str | None = None,
        fecha: datetime | None = None,
    ):
        self.descripcion = descripcion
        self.monto = monto
        self.tipo = tipo
        self.categoria = categoria
        self.fecha = fecha


# DTO de respuesta con los datos de un movimiento (incluye su ID)
class MovimientoRespuestaDTO:
    def __init__(
        self,
        id: int,
        descripcion: str,
        monto: Decimal,
        tipo: TipoMovimiento,
        categoria: str,
        fecha: datetime,
    ):
        self.id = id
        self.descripcion = descripcion
        self.monto = monto
        self.tipo = tipo
        self.categoria = categoria
        self.fecha = fecha


# DTO del balance: ingresos totales, gastos totales y saldo neto
class BalanceDTO:
    def __init__(self, ingresos: Decimal, gastos: Decimal, saldo: Decimal):
        self.ingresos = ingresos
        self.gastos = gastos
        self.saldo = saldo