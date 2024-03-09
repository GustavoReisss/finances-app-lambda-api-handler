import boto3
import os

__ddb_client = None

env = os.getenv("ENV", "local")

def setup_dynamodb_client():
    global __ddb_client

    params = {}

    if env == "local":
        params = {
            "endpoint_url": "http://localhost:8000",
            "region_name": "dummy",
            "aws_access_key_id": "dummy",
            "aws_secret_access_key": "dummy"
        }

    __ddb_client = boto3.resource(
        "dynamodb",
        **params
    )


def get_ddb_client():
    if not __ddb_client:
        setup_dynamodb_client()

    return __ddb_client