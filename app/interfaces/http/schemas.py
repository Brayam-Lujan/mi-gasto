from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict

from app.domain.models import TipoMovimiento


class MovimientoCreate(BaseModel):
    descripcion: str
    monto: Decimal
    tipo: TipoMovimiento
    categoria: str
    fecha: datetime

    model_config = ConfigDict(from_attributes=True)


class MovimientoUpdate(BaseModel):
    descripcion: Optional[str] = None
    monto: Optional[Decimal] = None
    tipo: Optional[TipoMovimiento] = None
    categoria: Optional[str] = None
    fecha: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class MovimientoResponse(BaseModel):
    id: int
    descripcion: str
    monto: Decimal
    tipo: TipoMovimiento
    categoria: str
    fecha: datetime

    model_config = ConfigDict(from_attributes=True)


class BalanceResponse(BaseModel):
    ingresos: Decimal
    gastos: Decimal
    saldo: Decimal

    model_config = ConfigDict(from_attributes=True)


class ErrorResponse(BaseModel):
    detail: str