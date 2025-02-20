from .despesa_futura_utils import gera_data_proxima_despesa, TODAY


def gera_data_proximo_pagamento(
    ultimaDespesa: str, frequencia: str, detalhes_frequencia: dict
):
    data_pagamento = gera_data_proxima_despesa(
        ultimaDespesa, frequencia, detalhes_frequencia
    )

    while TODAY > data_pagamento:
        data_pagamento = gera_data_proxima_despesa(
            data_pagamento, frequencia, detalhes_frequencia
        )

    return data_pagamento
