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


def getFirstWeekDayOfTheMonth(year, month, weekday: int | WeekdayEnum):
    first_day_of_the_month = date(year, month, 7)
    return first_day_of_the_month - relativedelta(
        days=(first_day_of_the_month.weekday() - WeekdayEnum(weekday).value) % 7
    )


TODAY = date.today()


def __gera_data_mensal(data_atual: date, detalhes_frequencia: dict):
    if not data_atual:
        return gera_data(
            TODAY.year, TODAY.month, int(detalhes_frequencia["diaPagamento"])
        )

    data_apos_um_mes = data_atual + relativedelta(months=1)
    return gera_data(
        data_apos_um_mes.year,
        data_apos_um_mes.month,
        int(detalhes_frequencia["diaPagamento"]),
    )  # Garante que será o dia selecionado ou o ultimo dia do mês


def __gera_data_semanal(data_atual: date, detalhes_frequencia: dict):
    if not data_atual:
        return getFirstWeekDayOfTheMonth(
            TODAY.year, TODAY.month, int(detalhes_frequencia["diaSemana"])
        )

    return data_atual + relativedelta(weeks=1)


def __gera_data_outras_frequencias(data_atual: date, detalhes_frequencia: dict):
    unidade = {"Dias": "days", "Semanas": "weeks", "Meses": "months", "Anos": "years"}[
        detalhes_frequencia["unidade"]
    ]

    increment = {f"{unidade}": int(detalhes_frequencia["quantidade"])}

    return data_atual + relativedelta(**increment)


__handlers = {
    f"{FrequenciaEnum.MENSAL.value}": __gera_data_mensal,
    f"{FrequenciaEnum.SEMANAL.value}": __gera_data_semanal,
    f"{FrequenciaEnum.OUTRO.value}": __gera_data_outras_frequencias,
}


def gera_data_proxima_despesa(
    data_despesa_atual: date | str | None, frequencia: str, detalhes_frequencia: dict
):
    if (
        data_despesa_atual and type(data_despesa_atual) is str
    ):  # Cenário onde a despesa possui ultima data de pagamento (no dynamoDB), devemos conferir se a mesma não está dentro do periodo solicitado
        return date(*[int(value) for value in data_despesa_atual.split("-")])

    return __handlers[FrequenciaEnum(frequencia).value](
        data_despesa_atual, detalhes_frequencia
    )
