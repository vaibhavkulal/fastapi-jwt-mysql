from __future__ import annotations

from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.core.security import (
    create_access_token,
    create_reset_token,
    hash_password,
    verify_password,
    verify_reset_token,
)
from app.models.user import User
from app.schemas.auth import LoginRequest, ResetPasswordRequest
from app.schemas.user import UserCreate, UserRegister, UserUpdate


def get_user_by_username(db: Session, username: str) -> User | None:
    return db.query(User).filter(User.username == username).first()


def get_user_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(User.email == email).first()


def get_user_by_identifier(db: Session, identifier: str) -> User | None:
    return db.query(User).filter(or_(User.username == identifier, User.email == identifier)).first()


def create_user(db: Session, payload: UserRegister | UserCreate, role: str = "USER") -> User:
    username_exists = get_user_by_username(db, payload.username)
    if username_exists:
        raise ValueError("username")

    email_exists = get_user_by_email(db, payload.email)
    if email_exists:
        raise ValueError("email")

    user_role = role if isinstance(payload, UserRegister) and not isinstance(payload, UserCreate) else getattr(payload, "role", role)
    user = User(
        username=payload.username,
        email=payload.email,
        password=hash_password(payload.password),
        role=user_role,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def authenticate_user(db: Session, login_data: LoginRequest) -> User | None:
    user = get_user_by_identifier(db, login_data.username_or_email)
    if not user:
        return None
    if not verify_password(login_data.password, user.password):
        return None
    return user


def build_access_token(user: User) -> str:
    return create_access_token(user)


def build_reset_token(user: User) -> str:
    return create_reset_token(user)


def reset_password(db: Session, payload: ResetPasswordRequest) -> User:
    user_id = verify_reset_token(payload.token)
    user = db.get(User, user_id)
    if not user:
        raise LookupError("user")
    user.password = hash_password(payload.new_password)
    db.commit()
    db.refresh(user)
    return user


def update_user(db: Session, user: User, payload: UserUpdate, allow_role_change: bool = False) -> User:
    data = payload.model_dump(exclude_unset=True)

    if "username" in data and data["username"] != user.username:
        if get_user_by_username(db, data["username"]):
            raise ValueError("username")
        user.username = data["username"]

    if "email" in data and data["email"] != user.email:
        if get_user_by_email(db, data["email"]):
            raise ValueError("email")
        user.email = data["email"]

    if "password" in data and data["password"]:
        user.password = hash_password(data["password"])

    if allow_role_change and "role" in data and data["role"]:
        user.role = data["role"]

    db.commit()
    db.refresh(user)
    return user


def delete_user(db: Session, user: User) -> None:
    db.delete(user)
    db.commit()