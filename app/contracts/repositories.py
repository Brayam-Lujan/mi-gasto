from abc import ABC, abstractmethod
from typing import List

from app.domain.models import Movimiento, TipoMovimiento


class IMovimientoRepository(ABC):
    """Contrato de persistencia para movimientos financieros.

    Los casos de uso dependen de esta interfaz, no de una implementación concreta.
    """

    @abstractmethod
    def guardar(self, movimiento: Movimiento) -> Movimiento:
        ...

    @abstractmethod
    def obtener_por_id(self, movimiento_id: int) -> Movimiento | None:
        ...

    @abstractmethod
    def listar(self) -> List[Movimiento]:
        ...

    @abstractmethod
    def actualizar(self, movimiento: Movimiento) -> Movimiento:
        ...

    @abstractmethod
    def eliminar(self, movimiento_id: int) -> bool:
        ...

    @abstractmethod
    def calcular_balance(self) -> dict:
        ...