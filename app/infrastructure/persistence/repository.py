from decimal import Decimal
from typing import List

from app.contracts.repositories import IMovimientoRepository
from app.domain.models import Movimiento, TipoMovimiento
from app.infrastructure.persistence.dbo.movimiento_dbo import MovimientoDBO
from app.infrastructure.persistence.mappers import MovimientoMapper
from app.config.database import SessionLocal


# Implementación concreta del repositorio usando SQLAlchemy
# Cumple el contrato IMovimientoRepository (inversión de dependencias)
class SQLAlchemyMovimientoRepository(IMovimientoRepository):

    def guardar(self, movimiento: Movimiento) -> Movimiento:
        db = SessionLocal()
        try:
            # Mapea dominio a DBO y lo inserta en la base de datos
            dbo = MovimientoMapper.to_dbo(movimiento)
            db.add(dbo)
            db.commit()
            db.refresh(dbo)  # Obtiene el ID autogenerado
            return MovimientoMapper.to_domain(dbo)
        finally:
            db.close()

    def obtener_por_id(self, movimiento_id: int) -> Movimiento | None:
        db = SessionLocal()
        try:
            dbo = (
                db.query(MovimientoDBO)
                .filter(MovimientoDBO.id == movimiento_id)
                .first()
            )
            if dbo is None:
                return None
            return MovimientoMapper.to_domain(dbo)
        finally:
            db.close()

    def listar(self) -> List[Movimiento]:
        db = SessionLocal()
        try:
            dbos = db.query(MovimientoDBO).all()
            return [MovimientoMapper.to_domain(dbo) for dbo in dbos]
        finally:
            db.close()

    def actualizar(self, movimiento: Movimiento) -> Movimiento:
        db = SessionLocal()
        try:
            dbo = (
                db.query(MovimientoDBO)
                .filter(MovimientoDBO.id == movimiento.id)
                .first()
            )
            if dbo is None:
                raise ValueError("Movimiento no encontrado para actualizar")
            # Actualiza campos del DBO con los valores de la entidad de dominio
            dbo.descripcion = movimiento.descripcion
            dbo.monto = movimiento.monto
            dbo.tipo = movimiento.tipo
            dbo.categoria = movimiento.categoria
            dbo.fecha = movimiento.fecha
            db.commit()
            db.refresh(dbo)
            return MovimientoMapper.to_domain(dbo)
        finally:
            db.close()

    def eliminar(self, movimiento_id: int) -> bool:
        db = SessionLocal()
        try:
            dbo = (
                db.query(MovimientoDBO)
                .filter(MovimientoDBO.id == movimiento_id)
                .first()
            )
            if dbo is None:
                return False
            db.delete(dbo)
            db.commit()
            return True
        finally:
            db.close()

    def calcular_balance(self) -> dict:
        db = SessionLocal()
        try:
            dbos = db.query(MovimientoDBO).all()
            ingresos = Decimal("0")
            gastos = Decimal("0")
            for dbo in dbos:
                monto = Decimal(str(dbo.monto))
                if dbo.tipo == TipoMovimiento.INGRESO:
                    ingresos += monto
                else:
                    gastos += monto
            saldo = ingresos - gastos
            return {"ingresos": ingresos, "gastos": gastos, "saldo": saldo}
        finally:
            db.close()