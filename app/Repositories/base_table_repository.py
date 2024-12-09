from dataclasses import dataclass
from Entities.Tables.base_table import Table
from env.ddb_client import get_ddb_client
from boto3.dynamodb.conditions import Key, Attr


@dataclass
class TableRepository:
    table: Table

    def __post_init__(self):
        self.__dynamo_table_instance = get_ddb_client().Table(self.table.name)

    @property
    def __dynamo_table(self):
        return self.__dynamo_table_instance

    def __build_filter_expression(self, filters: dict[str, str]) -> str:
        filters = [Attr(key).eq(value) for key, value in filters.items()]
        filter_expression = filters[0]

        for filter in filters[1:]:
            filter_expression = filter_expression & filter

        return filter_expression

    def get_all(
        self,
        filters: dict[str, str] = None,
        last_returned_keys: dict = None,
        limit: str | int = None,
    ):
        scan_params = {}

        if limit:
            scan_params["Limit"] = int(limit)

        if last_returned_keys:
            scan_params["ExclusiveStartKey"] = last_returned_keys

        if filters:
            scan_params["FilterExpression"] = self.__build_filter_expression(filters)

        scan_response = self.__dynamo_table.scan(**scan_params)

        return {
            "items": scan_response.get("Items", []),
            "lastReturnedKeys": scan_response.get("LastEvaluatedKey", {}),
        }

    def get_by_pk(self, pk, sk=""):
        filters = Key(self.table.partition_key).eq(pk)

        if sk and self.table.sort_key:
            filters = filters & Key(self.table.sort_key).eq(sk)

        query = self.__dynamo_table.query(KeyConditionExpression=filters)

        return query["Items"]

    def create_item(self, body):
        item = self.table.model(**body).model_dump()

        self.__dynamo_table.put_item(Item=item)

        return item

    def delete_item(self, pk, sk=""):
        if self.table.sort_key and not sk:
            raise Exception(
                f"Should use Partition Key and Sort Key for table {self.table.name}"
            )

        key = {self.table.partition_key: pk}

        if sk and self.table.sort_key:
            key[self.table.sort_key] = sk

        delete_response = self.__dynamo_table.delete_item(Key=key)

        return {
            "operationStatus": delete_response.get("ResponseMetadata", {}).get(
                "HTTPStatusCode"
            )
        }

    def update_item(self, pk, sk="", new_values={}):
        if self.table.sort_key and not sk:
            raise Exception(
                f"Should use Partition Key and Sort Key for table {self.table.name}"
            )

        if (
            self.table.partition_key in new_values
            and pk != str(new_values.get(self.table.partition_key, ""))
            or self.table.sort_key in new_values
            and sk != str(new_values.get(self.table.sort_key, ""))
        ):

            raise ValueError(
                f"the value of partition_key '{self.table.partition_key}'"
                f"{' or sort_key ' + self.table.sort_key if self.table.sort_key else ''} "
                f"in the body is different from partition_key '{pk}'"
                f"{' or sort_key ' + sk if self.table.sort_key else ''} "
                "present in request path"
            )

        current_value = self.get_by_pk(pk, sk)

        if not current_value:
            raise Exception(f"Item with pk: {pk} and sk: {sk} not found")

        updated_item = self.table.model(
            **{**current_value[0], **new_values}
        ).model_dump()

        self.__dynamo_table.put_item(Item=updated_item)

        return updated_item
