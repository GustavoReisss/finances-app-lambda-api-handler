from .generic_service import GenericService


class AtivosServicee(GenericService):

    def get(self, *args, **kwargs):
        ativos: list = super().get_by_pk_or_sk(first_arg=self.user_id)

        return ativos
