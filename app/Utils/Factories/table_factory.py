from Entities.Tables.tipo_pagamento_table import TipoPagamentoTable
from Entities.Tables.despesa_table import DespesaTable
from Entities.Tables.path_table import PathTable
from Utils.enums.endpoints import EndpointsEnum


class TableFactory:

    @staticmethod
    def create_table(endpoint: EndpointsEnum):
        tables = {
            EndpointsEnum.TIPOS_PAGAMENTOS: TipoPagamentoTable,
            EndpointsEnum.DESPESAS: DespesaTable,
            EndpointsEnum.ROTAS: PathTable,
        }

        return tables[endpoint]()
