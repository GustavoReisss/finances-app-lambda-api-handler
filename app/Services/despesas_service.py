from .generic_service import GenericService
from Utils.make_data_despesa import gera_data_proximo_pagamento
import uuid


class DespesasService(GenericService):

    def get(self, *args, **kwargs):
        return super().get_by_pk_or_sk(first_arg=self.user_request_info.userId)

    def post(self, body: dict):
        return super().post(
            {
                "userId": self.user_id,
                "despesaId": str(uuid.uuid4()),
                **self.normalize_body(body),
            }
        )

    def delete(self, first_arg, **kwargs):
        """
        first_arg == despesa_id
        """
        return super().delete(first_arg=self.user_id, second_arg=first_arg)

    def put(self, first_arg, body, **kwargs):
        """
        first_arg == despesa_id
        """
        return super().put(
            body=self.normalize_body(body), first_arg=self.user_id, second_arg=first_arg
        )

    def normalize_body(self, body: dict):
        body["dataProximoPagamento"] = self.__get_data_proximo_pagamento(body)
        return body

    def __get_data_proximo_pagamento(self, body: dict):
        if body.get("tipoPagamento") == "À Vista":
            return body.get("dataProximoPagamento")

        return gera_data_proximo_pagamento(
            body.get("ultimoPagamento"),
            body.get("frequencia"),
            body.get("detalhesFrequencia"),
        ).strftime("%Y-%m-%d")
