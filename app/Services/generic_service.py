import traceback
from pydantic import BaseModel
from Repositories.base_table_repository import TableRepository
from Entities.Utils.user_request_info import UserRequestInfo
from pydantic import ValidationError
from aws_lambda_powertools.event_handler.exceptions import (
    BadRequestError,
    InternalServerError,
)


class GenericService(BaseModel):
    table_repository: TableRepository
    user_request_info: UserRequestInfo

    @property
    def user_id(self):
        return self.user_request_info.userId

    def get(self):
        return self.table_repository.get_all()

    def get_by_pk_or_sk(self, first_arg, second_arg=""):
        return self.table_repository.get_by_pk(pk=first_arg, sk=second_arg)

    def post(self, body):
        try:
            return self.table_repository.create_item(body)

        except ValidationError as err:
            raise BadRequestError(str(err))

        except Exception as err:
            print(err, traceback.format_exc())
            raise InternalServerError("Internal Server Error")

    def put(self, body, first_arg, second_arg=""):
        try:
            return self.table_repository.update_item(
                pk=first_arg, sk=second_arg, new_values=body
            )
        except (ValidationError, ValueError) as err:
            raise BadRequestError(str(err))

        except Exception as err:
            print(err, traceback.format_exc())
            raise InternalServerError("Internal Server Error")

    def delete(self, first_arg, second_arg=""):
        return self.table_repository.delete_item(pk=first_arg, sk=second_arg)
