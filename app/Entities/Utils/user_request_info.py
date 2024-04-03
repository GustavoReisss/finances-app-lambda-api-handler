from pydantic import BaseModel


class UserRequestInfo(BaseModel):
    email: str
    expireOn: int
    sessionId: str
    userId: str
