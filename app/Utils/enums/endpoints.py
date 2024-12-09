from enum import Enum, auto


class EndpointsEnum(Enum):
    TIPOS_PAGAMENTOS = "tipos_pagamentos"
    DESPESAS = "despesas"
    ROTAS = "rotas"


if __name__ == "__main__":
    print(EndpointsEnum.TIPOS_PAGAMENTOS == EndpointsEnum("tipos_pagamentos"))
    print(type(EndpointsEnum("tipos_pagamentos")))
