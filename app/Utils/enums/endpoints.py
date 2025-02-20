from enum import Enum


class EndpointsEnum(Enum):
    TIPOS_PAGAMENTOS = "tipos_pagamentos"
    DESPESAS = "despesas"
    ATIVOS = "ativos"
    EXTRATO_DESPESAS = "extrato_despesas"


if __name__ == "__main__":
    print(EndpointsEnum.TIPOS_PAGAMENTOS == EndpointsEnum("tipos_pagamentos"))
    print(type(EndpointsEnum("tipos_pagamentos")))
