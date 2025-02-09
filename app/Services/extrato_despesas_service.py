from .generic_service import GenericService


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
