# Architecture

## High-Level Flow

```text
Client
  |
  v
FastAPI Router
  |
  v
Schema validation
  |
  v
Application/service logic
  |
  v
SQLAlchemy
  |
  v
MySQL
```

Authentication follows this general flow:

```text
Credentials
   |
   v
Authentication endpoint
   |
   v
Credential verification
   |
   v
JWT access token
   |
   v
Protected endpoint
   |
   v
Authenticated user
```

## Main Areas

- `app/core/` contains shared configuration and security concerns.
- `app/models/` contains SQLAlchemy database models.
- `app/schemas/` contains request and response validation models.
- `app/routers/` contains API route definitions.
- `app/services/` contains reusable application logic.
- `app/database.py` contains database configuration and session handling.
- `alembic/` contains versioned database migrations.
- `tests/` contains automated tests.

## Database Changes

Database schema changes should be made through SQLAlchemy models and generated/applied with Alembic. Direct manual schema changes are discouraged.
