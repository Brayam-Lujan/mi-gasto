from abc import ABC, abstractmethod
from typing import List

from app.domain.models import Movimiento, TipoMovimiento


# Contrato (interfaz) de persistencia para movimientos financieros.
# Los casos de uso dependen de esta interfaz, no de una implementación concreta (DIP).
class IMovimientoRepository(ABC):

    @abstractmethod
    def guardar(self, movimiento: Movimiento) -> Movimiento:
        """Guarda un movimiento y lo devuelve con su ID asignado."""
        ...

    @abstractmethod
    def obtener_por_id(self, movimiento_id: int) -> Movimiento | None:
        """Obtiene un movimiento por su ID o None si no existe."""
        ...

    @abstractmethod
    def listar(self) -> List[Movimiento]:
        """Lista todos los movimientos almacenados."""
        ...

    @abstractmethod
    def actualizar(self, movimiento: Movimiento) -> Movimiento:
        """Actualiza un movimiento existente y lo devuelve."""
        ...

    @abstractmethod
    def eliminar(self, movimiento_id: int) -> bool:
        """Elimina un movimiento por ID. Devuelve True si se eliminó."""
        ...

    @abstractmethod
    def calcular_balance(self) -> dict:
        """Calcula ingresos, gastos y saldo neto. Devuelve un diccionario."""
        ...