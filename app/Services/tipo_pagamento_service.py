from .generic_service import GenericService
import uuid


class TiposPagamentosService(GenericService):

    def get(self, *args, **kwargs):
        tipos_pagamentos: list = super().get_by_pk_or_sk(first_arg=self.user_id)

        if len(tipos_pagamentos) == 0:
            # New User, then create default values
            tipos_pagamentos = self.__create_default_tipos_pagamentos()

        return tipos_pagamentos

    def __create_default_tipos_pagamentos(self):
        default_tipo_pagamentos = ["À Vista", "Parcelado", "Recorrente"]

        return [
            self.table_repository.create_item(
                {
                    "userId": self.user_id,
                    "tipoPagamentoId": str(uuid.uuid4()),
                    "descricao": tipo_pagamento,
                    "categoriasPagamentos": [],
                }
            )[0]
            for tipo_pagamento in default_tipo_pagamentos
        ]

    def put(self, body, first_arg, **kwargs):
        return super().put(body, self.user_id, first_arg)

    def delete(self, first_arg, **kwargs):
        """
        first_arg == tipo_pagamento_id
        """
        return super().delete(first_arg=self.user_id, second_arg=first_arg)
