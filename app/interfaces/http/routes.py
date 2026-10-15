from decimal import Decimal
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

from app.application.dtos import (
    MovimientoActualizarDTO,
    MovimientoCrearDTO,
)
from app.application.use_cases.calcular_balance import CalcularBalance
from app.application.use_cases.crear_movimiento import CrearMovimiento
from app.application.use_cases.eliminar_movimiento import EliminarMovimiento
from app.application.use_cases.listar_movimientos import ListarMovimientos
from app.application.use_cases.obtener_movimiento import ObtenerMovimiento
from app.application.use_cases.actualizar_movimiento import ActualizarMovimiento
from app.config.database import SessionLocal, engine
from app.domain.models import TipoMovimiento
from app.infrastructure.persistence.repository import SQLAlchemyMovimientoRepository
from app.interfaces.http.schemas import (
    BalanceResponse,
    ErrorResponse,
    MovimientoCreate,
    MovimientoResponse,
    MovimientoUpdate,
)
from app.infrastructure.persistence.dbo.movimiento_dbo import MovimientoDBO
from app.config.database import Base

router = APIRouter()


def get_repository():
    db = SessionLocal()
    try:
        yield SQLAlchemyMovimientoRepository()
    finally:
        db.close()


@router.on_event("startup")
def crear_tablas():
    Base.metadata.create_all(bind=engine)


@router.post(
    "/movimientos",
    response_model=MovimientoResponse,
    status_code=status.HTTP_201_CREATED,
    responses={400: {"model": ErrorResponse}},
)
def crear_movimiento(
    datos: MovimientoCreate,
    repository=Depends(get_repository),
):
    caso_uso = CrearMovimiento(repository)
    dto = MovimientoCrearDTO(
        descripcion=datos.descripcion,
        monto=datos.monto,
        tipo=datos.tipo,
        categoria=datos.categoria,
        fecha=datos.fecha,
    )
    resultado = caso_uso.ejecutar(dto)
    return MovimientoResponse(
        id=resultado.id,
        descripcion=resultado.descripcion,
        monto=resultado.monto,
        tipo=resultado.tipo,
        categoria=resultado.categoria,
        fecha=resultado.fecha,
    )


@router.get(
    "/movimientos/{movimiento_id}",
    response_model=MovimientoResponse,
    responses={404: {"model": ErrorResponse}},
)
def obtener_movimiento(
    movimiento_id: int,
    repository=Depends(get_repository),
):
    caso_uso = ObtenerMovimiento(repository)
    try:
        resultado = caso_uso.ejecutar(movimiento_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    return MovimientoResponse(
        id=resultado.id,
        descripcion=resultado.descripcion,
        monto=resultado.monto,
        tipo=resultado.tipo,
        categoria=resultado.categoria,
        fecha=resultado.fecha,
    )


@router.get(
    "/movimientos",
    response_model=List[MovimientoResponse],
)
def listar_movimientos(repository=Depends(get_repository)):
    caso_uso = ListarMovimientos(repository)
    resultados = caso_uso.ejecutar()
    return [
        MovimientoResponse(
            id=r.id,
            descripcion=r.descripcion,
            monto=r.monto,
            tipo=r.tipo,
            categoria=r.categoria,
            fecha=r.fecha,
        )
        for r in resultados
    ]


@router.put(
    "/movimientos/{movimiento_id}",
    response_model=MovimientoResponse,
    responses={404: {"model": ErrorResponse}},
)
def actualizar_movimiento(
    movimiento_id: int,
    datos: MovimientoUpdate,
    repository=Depends(get_repository),
):
    caso_uso = ActualizarMovimiento(repository)
    dto = MovimientoActualizarDTO(
        descripcion=datos.descripcion,
        monto=datos.monto,
        tipo=datos.tipo,
        categoria=datos.categoria,
        fecha=datos.fecha,
    )
    try:
        resultado = caso_uso.ejecutar(movimiento_id, dto)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    return MovimientoResponse(
        id=resultado.id,
        descripcion=resultado.descripcion,
        monto=resultado.monto,
        tipo=resultado.tipo,
        categoria=resultado.categoria,
        fecha=resultado.fecha,
    )


@router.delete(
    "/movimientos/{movimiento_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={404: {"model": ErrorResponse}},
)
def eliminar_movimiento(
    movimiento_id: int,
    repository=Depends(get_repository),
):
    caso_uso = EliminarMovimiento(repository)
    try:
        caso_uso.ejecutar(movimiento_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    return None


@router.get(
    "/balance",
    response_model=BalanceResponse,
)
def calcular_balance(repository=Depends(get_repository)):
    caso_uso = CalcularBalance(repository)
    resultado = caso_uso.ejecutar()
    return BalanceResponse(
        ingresos=resultado.ingresos,
        gastos=resultado.gastos,
        saldo=resultado.saldo,
    )