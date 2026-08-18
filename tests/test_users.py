from __future__ import annotations

from app.core.security import create_access_token, hash_password
from app.models.user import User


def test_admin_can_list_users(client, db_session):
    admin = User(
        username="admin",
        email="admin@example.com",
        password=hash_password("Password@123"),
        role="ADMIN",
    )
    user = User(
        username="regular",
        email="regular@example.com",
        password=hash_password("Password@123"),
        role="USER",
    )
    db_session.add(admin)
    db_session.add(user)
    db_session.commit()
    db_session.refresh(admin)

    token = create_access_token(admin)

    response = client.get(
        "/api/users",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    assert len(response.json()) == 2


def test_user_cannot_access_another_profile(client, db_session):
    first_user = User(
        username="first",
        email="first@example.com",
        password=hash_password("Password@123"),
        role="USER",
    )
    second_user = User(
        username="second",
        email="second@example.com",
        password=hash_password("Password@123"),
        role="USER",
    )
    db_session.add(first_user)
    db_session.add(second_user)
    db_session.commit()
    db_session.refresh(first_user)
    db_session.refresh(second_user)

    token = create_access_token(first_user)

    response = client.get(
        f"/api/users/{second_user.id}",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 403