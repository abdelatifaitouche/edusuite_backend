import os
from dotenv import load_dotenv
import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from uuid import uuid4

from datetime import datetime, timedelta
from src.features.auth.schemas.jwt_payload import JwtPayload
from src.features.auth.exceptions import TokenExpiredError


class JwtManager:
    def __init__(self):
        self.ACCESS_TOKEN_TIME: int = 60 * 60  # in seconds
        self.REFRESH_TOKEN_TIME: int = 60 * 60 * 24 * 7  # one week in seconds

        secret: str | None = os.getenv("JWT_SECRET_KEY")

        if not secret:
            raise ValueError("JWT SECRET IS NOT SET IN THE ENV")

        self.SECRET_KEY = secret

        jwt_algo: str | None = os.getenv("JWT_ALG")

        if not jwt_algo:
            raise ValueError("JWT ALGO MUST BE SET IN ENV")

        self.JWT_ALG: str = jwt_algo

    def generate_token(
        self,
        payload: JwtPayload,
        is_refresh: bool = False,
    ) -> str:
        jwt_payload = {}

        jwt_payload["jti"] = str(uuid4())
        jwt_payload["iat"] = datetime.now()

        if is_refresh:
            jwt_payload["exp"] = datetime.now() + timedelta(
                seconds=self.REFRESH_TOKEN_TIME
            )
            jwt_payload["refresh"] = is_refresh
        else:
            jwt_payload["exp"] = datetime.now() + timedelta(
                seconds=self.ACCESS_TOKEN_TIME
            )
        jwt_payload["user_id"] = str(payload.id)
        jwt_payload["email"] = payload.email
        jwt_payload["role"] = payload.role
        encoded_jwt: str = jwt.encode(
            jwt_payload,
            self.SECRET_KEY,
            algorithm=self.JWT_ALG,
        )
        return encoded_jwt

    def verify_token(self, token: str) -> JwtPayload:
        try:
            decoded_token = jwt.decode(
                token,
                self.SECRET_KEY,
                algorithms=[
                    self.JWT_ALG,
                ],
            )
            jwt_payload: JwtPayload = JwtPayload(
                id=decoded_token["user_id"],
                email=decoded_token["email"],
                role=decoded_token["role"],
            )
            return jwt_payload
        except ExpiredSignatureError:
            raise TokenExpiredError()
        except InvalidTokenError:
            raise TokenExpiredError()
