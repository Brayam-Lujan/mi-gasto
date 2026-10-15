from datetime import datetime
from decimal import Decimal

from app.domain.models import TipoMovimiento


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


class BalanceDTO:
    def __init__(self, ingresos: Decimal, gastos: Decimal, saldo: Decimal):
        self.ingresos = ingresos
        self.gastos = gastos
        self.saldo = saldo