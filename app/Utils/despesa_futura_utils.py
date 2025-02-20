from datetime import date
from dateutil.relativedelta import relativedelta

from datetime import date
from dateutil.relativedelta import relativedelta
from enum import Enum


class FrequenciaEnum(Enum):
    MENSAL = "Mensal"
    SEMANAL = "Semanal"
    OUTRO = "Outro"


class WeekdayEnum(Enum):
    MONDAY = 0
    TUESDAY = 1
    WEDNESDAY = 2
    THURSDAY = 3
    FRIDAY = 4
    SATURDAY = 5
    SUNDAY = 6


def gera_data(ano: int, mes: int, dia: int):
    try:
        return date(ano, mes, dia)
    except ValueError:
        primeiro_dia_do_proximo_mes = date(ano, mes, 1) + relativedelta(months=1)
        return primeiro_dia_do_proximo_mes - relativedelta(days=1)


TODAY = date.today()


def __gera_data_mensal(detalhes_frequencia: dict):
    dia_pagamento = int(detalhes_frequencia["diaPagamento"])

    data_atual = TODAY

    if data_atual.day > dia_pagamento:
        data_atual = data_atual + relativedelta(months=1)

    return gera_data(data_atual.year, data_atual.month, int(dia_pagamento))


def __gera_data_semanal(detalhes_frequencia: dict):
    data_atual = TODAY

    if data_atual.weekday() == int(detalhes_frequencia["diaSemana"]):
        return data_atual

    while data_atual.weekday() != int(detalhes_frequencia["diaSemana"]):
        data_atual -= relativedelta(days=1)

    return data_atual + relativedelta(weeks=1)


def __gera_data_outras_frequencias(detalhes_frequencia: dict):
    unidade = {"Dias": "days", "Semanas": "weeks", "Meses": "months", "Anos": "years"}[
        detalhes_frequencia["unidade"]
    ]

    increment = {f"{unidade}": int(detalhes_frequencia["quantidade"])}

    return TODAY + relativedelta(**increment)


__handlers = {
    f"{FrequenciaEnum.MENSAL.value}": __gera_data_mensal,
    f"{FrequenciaEnum.SEMANAL.value}": __gera_data_semanal,
    f"{FrequenciaEnum.OUTRO.value}": __gera_data_outras_frequencias,
}


def gera_data_proxima_despesa(frequencia: str, detalhes_frequencia: dict) -> date:
    return __handlers[FrequenciaEnum(frequencia).value](detalhes_frequencia)
