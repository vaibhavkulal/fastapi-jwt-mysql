from __future__ import annotations

from datetime import datetime
from typing import Optional

from typing_extensions import Literal

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


def validate_password_strength(password: str) -> str:
    if len(password) < 8:
        raise ValueError("Password must be at least 8 characters long")
    if not any(character.islower() for character in password):
        raise ValueError("Password must contain a lowercase letter")
    if not any(character.isupper() for character in password):
        raise ValueError("Password must contain an uppercase letter")
    if not any(character.isdigit() for character in password):
        raise ValueError("Password must contain a digit")
    return password


class UserBase(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    email: EmailStr


class UserRegister(UserBase):
    password: str = Field(min_length=8, max_length=255)

    @field_validator("password")
    @classmethod
    def password_strength(cls, value: str) -> str:
        return validate_password_strength(value)


class UserCreate(UserRegister):
    role: Literal["USER", "ADMIN"] = "USER"


class UserUpdate(BaseModel):
    username: Optional[str] = Field(default=None, min_length=3, max_length=50)
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(default=None, min_length=8, max_length=255)
    role: Optional[Literal["USER", "ADMIN"]] = None

    @field_validator("password")
    @classmethod
    def password_strength(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return value
        return validate_password_strength(value)


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    email: EmailStr
    role: str
    created_at: datetime