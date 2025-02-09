from .base_table import Table, TableIndex
from ..Models.extrato_despesa_model import ExtratoDespesaModel, TableModel


class ExtratoDespesaTable(Table):
    name: str = "HistoricoDespesa"
    partition_key: str = "userId"
    sort_key: str = "despesaId"
    model: TableModel = ExtratoDespesaModel

    secondary_indexes: dict[str, TableIndex] = {
        "dataPagamentoIndex": TableIndex(
            name="dataPagamentoIndex", partition_key="userId", sort_key="dataPagamento"
        )
    }
