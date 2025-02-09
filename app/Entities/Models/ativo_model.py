from .base_table_model import TableModel


class AtivoModel(TableModel):
    userId: str
    codigo: str
    quantidade: str
    # categoriasPagamentos: list[str] = []
