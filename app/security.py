import hashlib

from fastapi import security
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt
from app.core.config import settings

algo = settings.jwt_algorithm
secret = settings.secret_key

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(
    plain_password: str,
    hashed_password: str
):
    return pwd_context.verify(
        plain_password,
        hashed_password
    )

def create_access_token(data: dict, expires_delta: int = 3600):
    
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(seconds=expires_delta)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, secret, algorithm=algo)
    return encoded_jwt

def create_refresh_token(data: dict, expires_delta: int = 604800):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(seconds=expires_delta)
    to_encode.update({"exp": expire, "type": "refresh"})
    encoded_jwt = jwt.encode(to_encode,secret, algorithm=algo)
    return encoded_jwt

def hash_token(token: str) -> str:
    return hashlib.sha256(token.encode()).hexdigest()
