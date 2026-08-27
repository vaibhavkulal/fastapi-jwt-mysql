# Database

## Database

The application uses MySQL for runtime persistence through SQLAlchemy.

## Migrations

Alembic is the source of truth for schema evolution.

Generate a migration after model changes:

```powershell
alembic revision --autogenerate -m "describe change"
```

Apply migrations:

```powershell
alembic upgrade head
```

Inspect migration state:

```powershell
alembic current
alembic history
```

## Test Database

The automated test suite uses an isolated SQLite database so tests can run without changing the local MySQL database.

## Rule

Do not edit the application database schema manually when the change can be represented by an Alembic migration.
