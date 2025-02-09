from .base_table import Table
from ..Models.ativo_model import AtivoModel, TableModel


class AtivoTable(Table):
    name: str = "ativos"
    partition_key: str = "userId"
    sort_key: str = "codigo "
    model: TableModel = AtivoModel
