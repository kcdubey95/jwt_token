import logging
from typing import Literal
from passlib.context import CryptContext
from jose import jwt, ExpiredSignatureError, JWTError
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
import datetime

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Constants for JWT
SECRET_KEY = "MIIBOgIBAAJBAKj34GkxFhD90vcNLYLInFEX6Ppy1tPf9Cnzj4p4WGeKLs1Pt8Qu"
ALGORITHM = "HS256"

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 scheme for obtaining a token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def create_credentials_exception(details: str):
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=details,
        headers={"WWW-Authenticate": "Bearer"},
    )


def access_token_expire_minutes() -> int:
    return 30


def create_access_token(email: str) -> str:
    logger.debug(f"Creating access token for email: {email}")
    expire = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(
        minutes=access_token_expire_minutes()
    )
    jwt_data = {"sub": email, "exp": expire, "type": "access"}
    encoded_jwt = jwt.encode(jwt_data, key=SECRET_KEY, algorithm=ALGORITHM)
    logger.debug(f"Access token created: {encoded_jwt}")
    return encoded_jwt


def verify_token(token: str, token_type: Literal["access", "confirmation"]) -> str:
    try:
        payload = jwt.decode(token, key=SECRET_KEY, algorithms=[ALGORITHM])
        logger.debug(f"Decoded JWT payload: {payload}")

        token_type_in_payload = payload.get("type")
        if token_type_in_payload != token_type:
            logger.error(f"Token type mismatch: expected {token_type}, got {token_type_in_payload}")
            raise create_credentials_exception("Token type mismatch")

        if 'sub' not in payload:
            logger.error("Token payload missing 'sub' field")
            raise create_credentials_exception("Token payload invalid")

        return payload.get("sub")
    except ExpiredSignatureError:
        logger.error("Token has expired")
        raise create_credentials_exception("Token has expired")
    except JWTError as e:
        logger.error(f"Invalid token: {e}")
        raise create_credentials_exception("Invalid token")


if __name__ == "__main__":
    try:
        email = "test@test.com"
        token = create_access_token(email)

        # Verify the token type (will raise an exception if there's an issue)
        verified_email = verify_token(token, "access")
        logger.info(f"Token is valid for user: {verified_email}")
    except HTTPException as e:
        logger.error(f"Token verification failed: {e.detail}")
