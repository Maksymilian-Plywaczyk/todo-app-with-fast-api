import os
from datetime import datetime, timedelta
from typing import Optional, Union

from dotenv import find_dotenv, load_dotenv
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from passlib.context import CryptContext

load_dotenv(find_dotenv())

# get secret key from environment variables should be kept secret
SECRET_KEY = os.getenv("SECRET_KEY")

ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 30

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# takes the plain password and returns the hash for it (stored in database)
def get_hashed_password(plain_password: str) -> str:
    return password_context.hash(plain_password)


# takes the plain and hashed passwords and validate them
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_context.verify(plain_password, hashed_password)


def create_access_token(
    subject: Union[str, any], expires_delta: Optional[timedelta] = None
) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )

    to_encode = {"exp": expires_delta, "subject": str(subject)}
    encoded_jwt = jwt.encode(claims=to_encode, key=SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def generate_reset_password_token(email: str) -> str:
    delta = timedelta(hours=ACCESS_TOKEN_EXPIRE_MINUTES)
    now = datetime.utcnow()
    expires = delta + now
    exp = expires.timestamp()
    to_encode = {"exp": exp, "subject": email}
    encoded_jwt = jwt.encode(claims=to_encode, key=SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_reset_password_token(token: str) -> Optional[str]:
    try:
        decoded_token = jwt.decode(token, key=SECRET_KEY, algorithms=[ALGORITHM])
        return decoded_token["subject"]
    except jwt.JWTError:
        return None
