from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import get_current_user, require_admin
from app.database import get_db
from app.models.user import User
from app.schemas.auth import MessageResponse
from app.schemas.user import UserCreate, UserResponse, UserUpdate
from app.services.auth import create_user, delete_user, update_user
from app.services.users import get_user, list_users

router = APIRouter(prefix="/api/users", tags=["users"])


@router.get("", response_model=List[UserResponse])
def read_users(_: User = Depends(require_admin), db: Session = Depends(get_db)):
    return list_users(db)


@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user_route(payload: UserCreate, _: User = Depends(require_admin), db: Session = Depends(get_db)):
    try:
        return create_user(db, payload, role=payload.role)
    except ValueError as exc:
        field = str(exc)
        if field == "username":
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username already exists") from exc
        if field == "email":
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already exists") from exc
        raise


@router.get("/me", response_model=UserResponse)
def read_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.get("/{user_id}", response_model=UserResponse)
def read_user(user_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    user = get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    if current_user.role != "ADMIN" and current_user.id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not allowed to access this user")

    return user


@router.put("/{user_id}", response_model=UserResponse)
def update_user_route(user_id: int, payload: UserUpdate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    user = get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    allow_role_change = current_user.role == "ADMIN"
    if not allow_role_change and current_user.id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not allowed to update this user")

    try:
        return update_user(db, user, payload, allow_role_change=allow_role_change)
    except ValueError as exc:
        field = str(exc)
        if field == "username":
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username already exists") from exc
        if field == "email":
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already exists") from exc
        raise


@router.delete("/{user_id}", response_model=MessageResponse)
def delete_user_route(user_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    user = get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    if current_user.role != "ADMIN" and current_user.id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not allowed to delete this user")

    delete_user(db, user)
    return MessageResponse(detail="User deleted successfully")