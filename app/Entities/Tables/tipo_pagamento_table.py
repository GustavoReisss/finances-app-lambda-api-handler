from .base_table import Table
from ..Models.tipo_pagamento_model import TipoPagamentoModel, TableModel

class TipoPagamentoTable(Table):
    name: str = "TipoPagamento"
    partition_key: str = "userId"
    sort_key: str = "tipoPagamentoId"
    model: TableModel = TipoPagamentoModel
