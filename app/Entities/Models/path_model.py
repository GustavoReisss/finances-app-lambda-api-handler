from .base_table_model import TableModel


class PathModel(TableModel):
    pathId: str
    comunidade: str
    releaseTrain: str
    squad: str
