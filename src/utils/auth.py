from enum import Enum
from uuid import UUID

import jwt
from pydantic import BaseModel, ValidationError

from core.config import settings


class TokenType(str, Enum):
    ACCESS = "access"
    REFRESH = "refresh"


class TokenPayload(BaseModel):
    iss: str
    type: TokenType
    iat: int
    exp: int


class AccessTokenPayload(TokenPayload):
    user_id: UUID
    user_login: str
    user_role: str


class AuthTokenError(Exception):
    pass


class AuthTokenValidationError(AuthTokenError):
    pass


class AuthTokenWrongTypeError(AuthTokenError):
    pass


def validate_token(token):
    try:
        token_payload = jwt.decode(
            token,
            settings.public_key,
            algorithms=[settings.token_algorithm],
            leeway=30,
        )
        access_token = AccessTokenPayload(**token_payload)
    except (jwt.exceptions.DecodeError, ValidationError):
        raise AuthTokenError
    if access_token.type != TokenType.ACCESS:
        raise AuthTokenWrongTypeError
    return access_token
