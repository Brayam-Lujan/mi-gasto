from app.application.dtos import BalanceDTO
from app.contracts.repositories import IMovimientoRepository


class CalcularBalance:
    def __init__(self, repository: IMovimientoRepository):
        self._repository = repository

    def ejecutar(self) -> BalanceDTO:
        datos = self._repository.calcular_balance()
        return BalanceDTO(
            ingresos=datos["ingresos"],
            gastos=datos["gastos"],
            saldo=datos["saldo"],
        )