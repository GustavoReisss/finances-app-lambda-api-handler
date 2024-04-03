from Entities.Utils.user_request_info import UserRequestInfo


def get_user_info(event: dict) -> UserRequestInfo:
    return UserRequestInfo(
        **event.get("requestContext", {}).get("authorizer", {}).get("lambda", {})
    )
