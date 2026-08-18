from __future__ import annotations

from sqlalchemy.orm import Session

from app.models.user import User


def list_users(db: Session) -> list[User]:
    return db.query(User).order_by(User.id.asc()).all()


def get_user(db: Session, user_id: int) -> User | None:
    return db.get(User, user_id)