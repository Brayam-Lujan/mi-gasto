from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict

from app.domain.models import TipoMovimiento


# Esquema Pydantic para validar el cuerpo de solicitud al crear un movimiento (POST /movimientos)
class MovimientoCreate(BaseModel):
    descripcion: str
    monto: Decimal
    tipo: TipoMovimiento
    categoria: str
    fecha: datetime

    model_config = ConfigDict(from_attributes=True)


# Esquema Pydantic para validar el cuerpo de solicitud al actualizar un movimiento (PUT /movimientos/{id})
class MovimientoUpdate(BaseModel):
    descripcion: Optional[str] = None
    monto: Optional[Decimal] = None
    tipo: Optional[TipoMovimiento] = None
    categoria: Optional[str] = None
    fecha: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


# Esquema Pydantic para la respuesta de un movimiento (incluye su ID asignado)
class MovimientoResponse(BaseModel):
    id: int
    descripcion: str
    monto: Decimal
    tipo: TipoMovimiento
    categoria: str
    fecha: datetime

    model_config = ConfigDict(from_attributes=True)


# Esquema Pydantic para la respuesta del balance (ingresos, gastos, saldo neto)
class BalanceResponse(BaseModel):
    ingresos: Decimal
    gastos: Decimal
    saldo: Decimal

    model_config = ConfigDict(from_attributes=True)


# Esquema Pydantic para respuestas de error
class ErrorResponse(BaseModel):
    detail: str