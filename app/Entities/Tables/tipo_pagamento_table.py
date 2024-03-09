from .base_table import Table
from ..Models.tipo_pagamento_model import TipoPagamentoModel, TableModel

class TipoPagamentoTable(Table):
    partition_key: str = "UserId"
    name: str = "TipoPagamento"
    sort_key: str = "TipoPagamentoId"
    model: TableModel = TipoPagamentoModel
