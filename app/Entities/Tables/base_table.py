from pydantic import BaseModel
from ..Models.base_table_model import TableModel


class TableIndex(BaseModel):
    name: str
    partition_key: str
    sort_key: str = ""


class Table(TableIndex):
    model: TableModel

    secondary_indexes: dict[str, TableIndex] = {}
