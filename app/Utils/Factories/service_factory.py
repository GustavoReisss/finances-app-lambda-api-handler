from Services.generic_service import GenericService
from Services.tipo_pagamento_service import TiposPagamentosService
from Services.despesas_service import DespesasService
from .repository_factory import RepositoryFactory
from aws_lambda_powertools.event_handler.exceptions import NotFoundError
from Utils.enums.endpoints import EndpointsEnum
from Entities.Utils.user_request_info import UserRequestInfo


class ServiceFactory:

    @staticmethod
    def create_service(endpoint: str | EndpointsEnum, user_info: UserRequestInfo):
        # use to map endpoints that have custom services
        custom_services: dict[EndpointsEnum, GenericService] = {
            EndpointsEnum.TIPOS_PAGAMENTOS: TiposPagamentosService,
            EndpointsEnum.DESPESAS: DespesasService,
        }

        try:
            endpoint = EndpointsEnum(endpoint)

            repository = RepositoryFactory.create_repository(endpoint)
        except (KeyError, ValueError):
            raise NotFoundError

        return custom_services.get(endpoint, GenericService)(
            table_repository=repository, user_request_info=user_info
        )
