from .generic_service import GenericService
import uuid


class ExtratoDespesasService(GenericService):

    def get_by_pk_or_sk(self, first_arg, second_arg=""):
        return self.table_repository.get_by_pk(pk=first_arg, sk=second_arg)

    def get(self, *args, **kwargs):
        query_params = kwargs.get("query_params") or {}
        order = query_params.get("order", "asc")

        sk = query_params.get("beforeDate", "")

        return self.table_repository.get_by_pk(
            pk=self.user_request_info.userId,
            sk=sk,
            index_name="dataPagamentoIndex",
            order_by=order,
            sk_filter_operator="lte",
        )

    def delete(self, *args, **kwargs):
        return self.table_repository.delete_item(
            pk=self.user_request_info.userId, sk=kwargs["first_arg"]
        )

    def post(self, body):
        body["userId"] = self.user_request_info.userId
        body["despesaId"] = str(uuid.uuid4())

        return self.table_repository.create_item(body=body)

    def put(self, body, **kwargs):
        return super().put(
            body=body,
            first_arg=self.user_request_info.userId,
            second_arg=kwargs["first_arg"],
        )
