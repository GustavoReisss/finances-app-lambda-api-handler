from Entities.Tables.tipo_pagamento_table import TipoPagamentoTable
from Entities.Tables.despesa_table import DespesaTable
from Entities.Tables.extrato_despesa_table import ExtratoDespesaTable
from Entities.Tables.ativo_table import AtivoTable
from Utils.enums.endpoints import EndpointsEnum


class TableFactory:

    @staticmethod
    def create_table(endpoint: EndpointsEnum):
        tables = {
            EndpointsEnum.TIPOS_PAGAMENTOS: TipoPagamentoTable,
            EndpointsEnum.DESPESAS: DespesaTable,
            EndpointsEnum.ATIVOS: AtivoTable,
            EndpointsEnum.EXTRATO_DESPESAS: ExtratoDespesaTable,
        }

        return tables[endpoint]()
