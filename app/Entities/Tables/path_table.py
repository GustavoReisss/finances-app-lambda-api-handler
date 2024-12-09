from .base_table import Table
from ..Models.path_model import PathModel, TableModel


class PathTable(Table):
    name: str = "Paths"
    partition_key: str = "pathId"
    model: TableModel = PathModel
