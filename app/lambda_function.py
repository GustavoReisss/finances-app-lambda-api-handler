import json
import traceback
from Utils.Factories.repository_factory import get_repository
from pydantic import ValidationError
from aws_lambda_powertools.event_handler import ApiGatewayResolver
from aws_lambda_powertools.event_handler.exceptions import BadRequestError, InternalServerError

api_gateway_resolver = ApiGatewayResolver()

@api_gateway_resolver.get("/<endpoint>")
def get(endpoint):    
    return get_repository(endpoint).get_all()

@api_gateway_resolver.get("/<endpoint>/<partition_key>")
@api_gateway_resolver.get("/<endpoint>/<partition_key>/<sort_key>")
def get_by_pk_or_sk(endpoint, partition_key="", sort_key=""):
    return get_repository(endpoint).get_by_pk(pk=partition_key, sk=sort_key)

@api_gateway_resolver.post("/<endpoint>")
def post(endpoint):
    body = api_gateway_resolver.current_event.body
    
    try:
        return get_repository(endpoint).create_item(body)
    
    except ValidationError as err:
        raise BadRequestError(str(err))
    
    except Exception as err:
        raise InternalServerError("Internal Server Error")

@api_gateway_resolver.put("/<endpoint>/<partition_key>")
@api_gateway_resolver.put("/<endpoint>/<partition_key>/<sort_key>")
def put(endpoint, partition_key="", sort_key=""):
    body = api_gateway_resolver.current_event.body
    
    try:
        return get_repository(endpoint).update_item(pk=partition_key, sk=sort_key, new_values=body)
    
    except (ValidationError, ValueError) as err:
        raise BadRequestError(str(err))
    
    except Exception as err:
        print(err, traceback.format_exc())
        raise InternalServerError("Internal Server Error")


@api_gateway_resolver.delete("/<endpoint>/<partition_key>")
@api_gateway_resolver.delete("/<endpoint>/<partition_key>/<sort_key>")
def delete(endpoint, partition_key="", sort_key=""):
    return get_repository(endpoint).delete_item(pk=partition_key, sk=sort_key)


def lambda_handler(event, context = None):
    # return api_gateway_resolver.resolve(event, context)

    response = api_gateway_resolver.resolve(event, context)
    
    if "body" in response:
        response["body"] = json.loads(response["body"])

    return response