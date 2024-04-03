from Repositories.base_table_repository import TableRepository
from .table_factory import TableFactory
from aws_lambda_powertools.event_handler.exceptions import NotFoundError
from Utils.enums.endpoints import EndpointsEnum


class RepositoryFactory:

    @staticmethod
    def create_repository(endpoint: str | EndpointsEnum):
        # use to map endpoints that have custom repositories
        custom_repositories: dict[EndpointsEnum, TableRepository] = {}

        try:
            endpoint = EndpointsEnum(endpoint)

            table = TableFactory.create_table(endpoint)
        except (KeyError, ValueError) as err:
            print(err)
            raise NotFoundError

        repository = custom_repositories.get(endpoint, TableRepository)(table=table)

        return repository
