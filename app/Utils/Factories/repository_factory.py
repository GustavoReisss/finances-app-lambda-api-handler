from Repositories.base_table_repository import TableRepository
from .table_factory import get_table
from aws_lambda_powertools.event_handler.exceptions import NotFoundError


def get_repository(endpoint: str):
    mapped_repositores: dict[str, TableRepository] = {}

    try:
        table = get_table(endpoint)
    except KeyError:
        raise NotFoundError
    
    repository = mapped_repositores.get(endpoint, TableRepository)(table=table)
    
    return repository