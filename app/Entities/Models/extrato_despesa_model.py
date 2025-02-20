from .base_table_model import TableModel
from decimal import Decimal


class ExtratoDespesaModel(TableModel):
    userId: str
    despesaId: str
    descricao: str
    valor: Decimal
    dataPagamento: str
    categoriaPagamento: str = ""
    tipoPagamento: str = ""
