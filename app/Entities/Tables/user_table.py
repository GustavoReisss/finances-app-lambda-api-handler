from .base_table import Table
from ..Models.user_model import UserModel, TableModel

class UserTable(Table):
    partition_key: str = "id"
    name: str = "User"
    model: TableModel = UserModel