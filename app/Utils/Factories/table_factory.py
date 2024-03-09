from Entities.Tables.user_table import UserTable
from Entities.Tables.tipo_pagamento_table import TipoPagamentoTable

def get_table(endpoint: str):
    tables = {
        "user": UserTable,
        "tipoPagamento": TipoPagamentoTable
    }

    return tables[endpoint]()