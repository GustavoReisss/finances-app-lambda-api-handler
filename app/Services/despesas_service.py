from .generic_service import GenericService


class DespesasService(GenericService):

    def get(self):
        return super().get_by_pk_or_sk(first_arg=self.user_request_info.userId)

    def post(self, body):
        return super().post({"userId": self.user_id, **body})

    def delete(self, first_arg, **kwargs):
        """
        first_arg == despesa_id
        """
        return super().delete(first_arg=self.user_id, second_arg=first_arg)

    def put(self, first_arg, body, **kwargs):
        """
        first_arg == despesa_id
        """
        return super().put(body=body, first_arg=self.user_id, second_arg=first_arg)
