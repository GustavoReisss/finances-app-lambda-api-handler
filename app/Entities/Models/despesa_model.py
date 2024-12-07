from decimal import Decimal
from .base_table_model import TableModel, BaseModel
from enum import Enum
from pydantic import model_validator


class TipoPagamentoEnum(str, Enum):
    recorrente = "Recorrente"
    parcelado = "Parcelado"
    a_vista = "À Vista"


class FrequenciaEnum(str, Enum):
    mensal = "Mensal"
    semanal = "Semanal"
    outro = "Outro"


class DespesaModel(TableModel):
    userId: str
    despesaId: str
    tipoPagamento: TipoPagamentoEnum
    categoriaPagamento: str
    ultimoPagamento: str
    descricao: str
    valor: Decimal
    dataProximoPagamento: str = ""

    @model_validator(mode="before")
    def validate_tipo_pagamento_extra_fields(cls, data):
        tipo_pagamento_validation_handlers = {
            f"{TipoPagamentoEnum.parcelado.value}": cls.__check_despesa_parcelada,
            f"{TipoPagamentoEnum.recorrente.value}": cls.__check_despesa_recorrente,
        }

        tipo_pagamento = data.get("tipoPagamento")

        if tipo_pagamento in tipo_pagamento_validation_handlers:
            tipo_pagamento_validation_handlers[tipo_pagamento](data)

        return data

    @staticmethod
    def __check_despesa_parcelada(data: dict):
        class DespesaParcelada(BaseModel):
            quantidadeParcelas: int
            parcelaAtual: int
            frequencia: FrequenciaEnum
            detalhesFrequencia: dict

        DespesaParcelada(
            quantidadeParcelas=data.get("quantidadeParcelas"),
            parcelaAtual=data.get("parcelaAtual"),
            frequencia=data.get("frequencia"),
            detalhesFrequencia=data.get("detalhesFrequencia"),
        )

    @staticmethod
    def __check_despesa_recorrente(data: dict):
        class DespesaRecorrente(BaseModel):
            frequencia: FrequenciaEnum
            detalhesFrequencia: dict

        DespesaRecorrente(
            frequencia=data.get("frequencia"),
            detalhesFrequencia=data.get("detalhesFrequencia"),
        )
