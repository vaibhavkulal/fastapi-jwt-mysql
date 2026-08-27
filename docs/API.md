# API Reference

The running FastAPI application exposes interactive documentation at `/docs` and an OpenAPI schema at `/openapi.json`.

## Authentication

| Method | Endpoint | Purpose |
|---|---|---|
| POST | `/api/auth/register` | Register a user |
| POST | `/api/auth/login` | Authenticate and receive a JWT |
| POST | `/api/auth/token` | OAuth2-compatible token flow |
| GET | `/api/auth/me` | Get the authenticated user |
| POST | `/api/auth/forgot-password` | Start password reset |
| POST | `/api/auth/reset-password` | Reset a password |

## Users

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/api/users` | List users |
| POST | `/api/users` | Create a user |
| GET | `/api/users/{user_id}` | Get a user |
| PUT | `/api/users/{user_id}` | Update a user |
| DELETE | `/api/users/{user_id}` | Delete a user |

Authorization requirements depend on the endpoint and configured user role.

## API Documentation

Run the application locally with:

```powershell
uvicorn app.main:app --reload
```

Then open:

```text
http://127.0.0.1:8000/docs
```
