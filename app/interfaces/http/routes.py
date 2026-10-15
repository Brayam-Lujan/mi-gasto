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
from app.domain.models import Movimiento, TipoMovimiento
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
from datetime import datetime
from decimal import Decimal

router = APIRouter()


# Inyección de dependencia: provee una instancia del repositorio concreto por petición
def get_repository():
    db = SessionLocal()
    try:
        yield SQLAlchemyMovimientoRepository()
    finally:
        db.close()


# Crea las tablas en la base de datos al iniciar la aplicación
# y carga datos de ejemplo si la tabla está vacía (base de datos en memoria recién iniciada)
@router.on_event("startup")
def crear_tablas():
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        repo = SQLAlchemyMovimientoRepository()
        # Solo insertar datos de ejemplo si no hay movimientos registrados
        if not repo.listar():
            datos_iniciales = [
                Movimiento(
                    id=None,
                    descripcion="Salario mensual",
                    monto=Decimal("1500.00"),
                    tipo=TipoMovimiento.INGRESO,
                    categoria="Trabajo",
                    fecha=datetime(2026, 10, 15, 8, 0, 0),
                ),
                Movimiento(
                    id=None,
                    descripcion="Trabajo freelance",
                    monto=Decimal("500.00"),
                    tipo=TipoMovimiento.INGRESO,
                    categoria="Trabajo",
                    fecha=datetime(2026, 10, 14, 8, 0, 0),
                ),
                Movimiento(
                    id=None,
                    descripcion="Supermercado",
                    monto=Decimal("85.50"),
                    tipo=TipoMovimiento.GASTO,
                    categoria="Alimentación",
                    fecha=datetime(2026, 10, 15, 9, 0, 0),
                ),
                Movimiento(
                    id=None,
                    descripcion="Transporte público",
                    monto=Decimal("30.00"),
                    tipo=TipoMovimiento.GASTO,
                    categoria="Transporte",
                    fecha=datetime(2026, 10, 15, 10, 0, 0),
                ),
                Movimiento(
                    id=None,
                    descripcion="Servicios básicos",
                    monto=Decimal("120.00"),
                    tipo=TipoMovimiento.GASTO,
                    categoria="Hogar",
                    fecha=datetime(2026, 10, 13, 8, 0, 0),
                ),
            ]
            for movimiento in datos_iniciales:
                repo.guardar(movimiento)
    finally:
        db.close()


# POST /movimientos: crea un nuevo movimiento financiero
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


# GET /movimientos/{id}: obtiene un movimiento por su ID
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


# GET /movimientos: lista todos los movimientos
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


# PUT /movimientos/{id}: actualiza un movimiento existente (campos opcionales)
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


# DELETE /movimientos/{id}: elimina un movimiento por su ID
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


# GET /balance: calcula ingresos, gastos y saldo neto
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