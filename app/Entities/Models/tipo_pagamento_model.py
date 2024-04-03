from .base_table_model import TableModel

class TipoPagamentoModel(TableModel):
    userId: str
    tipoPagamentoId: str
    descricao: str
    categoriasPagamentos: list[str] = []