# FastAPI JWT MySQL

A local-only FastAPI project that uses SQLAlchemy, Alembic, and MySQL to build authentication and user management features.

## What is included

- FastAPI application
- MySQL connection through SQLAlchemy
- Alembic migrations
- User registration
- Login with JWT access tokens
- Protected profile endpoint
- Forgot password and reset password flow
- User CRUD with role-based authorization
- Automated tests

## Project structure

```text
fastapi-jwt-mysql/
├── app/
│   ├── core/
│   ├── models/
│   ├── routers/
│   ├── schemas/
│   ├── services/
│   ├── database.py
│   └── main.py
├── alembic/
├── tests/
├── .env
├── .env.example
├── alembic.ini
├── requirements.txt
└── README.md
```

## Requirements

- Python
- MySQL Server
- MySQL Workbench, optional
- A virtual environment named `venv`

## 1. Create and activate the virtual environment

From the project root on Windows:

```powershell
python -m venv venv
venv\Scripts\activate
```

If your project already has `venv`, just activate it.

## 2. Install dependencies

```powershell
pip install -r requirements.txt
```

## 3. Configure environment variables

Create a `.env` file in the project root if it does not already exist.

Example:

```env
DB_HOST=localhost
DB_PORT=3306
DB_NAME=fastapi_auth
DB_USER=root
DB_PASSWORD=your_password
JWT_SECRET=change-this-secret
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
RESET_TOKEN_EXPIRE_MINUTES=15
```

You can copy `.env.example` and fill in your own values.

## 4. Create the MySQL database

Create a database in MySQL first:

```sql
CREATE DATABASE fastapi_auth;
```

Make sure the name matches `DB_NAME` in `.env`.

## 5. Run Alembic migrations

The database schema is managed through Alembic.

Generate a migration if the model changes:

```powershell
alembic revision --autogenerate -m "message here"
```

Apply migrations:

```powershell
alembic upgrade head
```

Check migration history:

```powershell
alembic current
alembic history
```

## 6. Start the API server

Run the app with Uvicorn:

```powershell
uvicorn app.main:app --reload
```

Open these in your browser:

- API docs: http://127.0.0.1:8000/docs
- OpenAPI schema: http://127.0.0.1:8000/openapi.json
- Root check: http://127.0.0.1:8000/
- Database test: http://127.0.0.1:8000/db-test

## 7. How to use the API

## Password security

Passwords are never stored directly in MySQL.

Flow:

```text
User password
  ↓
bcrypt hash
  ↓
MySQL
```

The app uses `passlib[bcrypt]` through `app/core/security.py`.

### Register a user

POST `/api/auth/register`

Example body:

```json
{
  "username": "vaibhav",
  "email": "vaibhav@example.com",
  "password": "Password@123"
}
```

### Login

POST `/api/auth/login`

Example body:

```json
{
  "username_or_email": "vaibhav",
  "password": "Password@123"
}
```

Response includes an access token:

```json
{
  "access_token": "eyJ...",
  "token_type": "bearer"
}
```

### Use the token

You have two options:

1. Use the JSON login endpoint above, copy the token, then click Authorize in Swagger and paste:

```text
Bearer your_access_token
```

2. Or use Swagger's built-in OAuth2 login:

  - Open `/docs`
  - Click `Authorize`
  - Enter your username and password
  - Swagger will call `POST /api/auth/token` automatically

### Get current user

GET `/api/auth/me`

Requires a valid JWT token.

### Forgot password

POST `/api/auth/forgot-password`

Example body:

```json
{
  "email": "vaibhav@example.com"
}
```

### Reset password

POST `/api/auth/reset-password`

Example body:

```json
{
  "token": "reset-token-here",
  "new_password": "NewPassword@123"
}
```

### User CRUD

- GET `/api/users`
- POST `/api/users`
- GET `/api/users/{user_id}`
- PUT `/api/users/{user_id}`
- DELETE `/api/users/{user_id}`

Admin access is required for listing all users and creating users through the user router.

## 8. Run tests

```powershell
pytest -q
```

The test suite uses an isolated SQLite test database.

## 9. Common workflow

1. Update the SQLAlchemy model in `app/models/user.py`
2. Generate a migration with Alembic
3. Apply the migration
4. Update schemas or routes if needed
5. Run tests

## 10. Notes

- Docker is intentionally not part of this project.
- Do not edit the database schema manually.
- Use Alembic for every schema change.
- The project currently runs on the existing Python environment in `venv`.

## Useful commands

```powershell
venv\Scripts\activate
pip install -r requirements.txt
alembic revision --autogenerate -m "create users table"
alembic upgrade head
uvicorn app.main:app --reload
pytest -q
```

## Current status

- FastAPI project setup: done
- MySQL connection: done
- Environment config: done
- Database dependency: done
- User model: done
- Alembic setup: done
- First migration: done
- Schemas, auth, JWT, CRUD, roles, and tests: done
- Docker: skipped by request
