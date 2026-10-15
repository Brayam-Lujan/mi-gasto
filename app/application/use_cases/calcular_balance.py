from app.application.dtos import BalanceDTO
from app.contracts.repositories import IMovimientoRepository


# Caso de uso: calcula el balance financiero (ingresos, gastos, saldo neto)
class CalcularBalance:
    def __init__(self, repository: IMovimientoRepository):
        self._repository = repository

    def ejecutar(self) -> BalanceDTO:
        # Obtiene los datos del balance desde el repositorio
        datos = self._repository.calcular_balance()
        # Retorna DTO con ingresos, gastos y saldo neto
        return BalanceDTO(
            ingresos=datos["ingresos"],
            gastos=datos["gastos"],
            saldo=datos["saldo"],
        )