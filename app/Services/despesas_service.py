from .generic_service import GenericService


class DespesasService(GenericService):

    def get(self):
        return super().get_by_pk_or_sk(first_arg=self.user_request_info.userId)

    def post(self, body):
        return super().post({"userId": self.user_id, **body})
