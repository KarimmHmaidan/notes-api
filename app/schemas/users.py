from pydantic import BaseModel, EmailStr, field_validator
from datetime import datetime
import re

class UserCreate(BaseModel):
    username: str 
    email: EmailStr
    password: str

    @field_validator("username")
    def username_restrictions(cls, value: str) -> str:
        if  len(value) < 4 :
            raise ValueError("username must be at least 4 characters long")
        if  len(value) > 30 :
            raise ValueError("username must be no more than 30 characters long")
        if value.startswith("_") or value.endswith("_"):
            raise ValueError("username cannot start or end with an underscore")
        if  not  re.match(r'^[a-zA-Z0-9_]+$', value):
            raise ValueError("username can only contain letters, numbers, underscores")
        return value
    @field_validator("password")
    def password_restrictions(cls, value: str) -> str:
        if len(value) < 8:
            raise ValueError("password must be at least 8 characters long")
        if len(value) > 128:
            raise ValueError("password must be no more than 128 characters long")
        if not re.search(r'[0-9]', value):
            raise ValueError("password must contain at least one number")
        if re.match(r'^[\s]+$', value):
            raise ValueError("password cannot contain only whitespace characters")
        return value

class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    login_identifier: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class RefreshTokenRequest(BaseModel):
    refresh_token: str




