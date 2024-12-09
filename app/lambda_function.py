import json
from Utils.Factories.service_factory import ServiceFactory
from Utils.get_user_info import get_user_info
from aws_lambda_powertools.event_handler import APIGatewayHttpResolver, CORSConfig
from aws_lambda_powertools.event_handler.api_gateway import Router


cors_config = CORSConfig(allow_credentials=True)
resolver = APIGatewayHttpResolver(cors=cors_config)

router = Router()


@router.get("/<endpoint>")
def get(endpoint):
    user_info = router.context.get("user")
    query_params = resolver.current_event.query_string_parameters

    return ServiceFactory.create_service(endpoint=endpoint, user_info=user_info).get(
        query_params=query_params
    )


@router.get("/<endpoint>/<first_arg>")
@router.get("/<endpoint>/<first_arg>/<second_arg>")
def get_by_pk_or_sk(endpoint, first_arg="", second_arg=""):
    user_info = router.context.get("user")

    return ServiceFactory.create_service(
        endpoint=endpoint, user_info=user_info
    ).get_by_pk_or_sk(first_arg=first_arg, second_arg=second_arg)


@router.post("/<endpoint>")
def post(endpoint):
    body = resolver.current_event.body
    user_info = router.context.get("user")

    return ServiceFactory.create_service(endpoint=endpoint, user_info=user_info).post(
        body
    )


@router.put("/<endpoint>/<first_arg>")
@router.put("/<endpoint>/<first_arg>/<second_arg>")
def put(endpoint, first_arg="", second_arg=""):
    body = resolver.current_event.body
    user_info = router.context.get("user")

    return ServiceFactory.create_service(endpoint=endpoint, user_info=user_info).put(
        body=body, first_arg=first_arg, second_arg=second_arg
    )


@router.delete("/<endpoint>/<first_arg>")
@router.delete("/<endpoint>/<first_arg>/<second_arg>")
def delete(endpoint, first_arg="", second_arg=""):
    user_info = router.context.get("user")

    return ServiceFactory.create_service(endpoint=endpoint, user_info=user_info).delete(
        first_arg=first_arg, second_arg=second_arg
    )


resolver.include_router(router, prefix="")


def lambda_handler(event, context=None):
    resolver.append_context(user=get_user_info(event))

    if "body" in event and type(event["body"]) is str:
        event["body"] = json.loads(event["body"])

    return resolver.resolve(event, context)
