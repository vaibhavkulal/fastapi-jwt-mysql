# Project Overview

## What is this project?

`fastapi-jwt-mysql` is a local FastAPI authentication and user-management project built with SQLAlchemy, Alembic, and MySQL.

## Why does it exist?

The project provides a practical reference implementation for learning and developing backend features around authentication, authorization, database migrations, JWT security, and user management.

## Goals

- Keep the backend structure simple and maintainable.
- Use Alembic for versioned database schema changes.
- Keep authentication and authorization concerns separated from API routing.
- Provide automated tests for backend behavior.
- Keep project documentation close to the code and continuously updated.

## Technology Stack

- Python
- FastAPI
- SQLAlchemy
- MySQL
- Alembic
- JWT
- Pytest

## Current Scope

The current application includes user registration, JWT login, protected user/profile access, password reset flows, user CRUD, role-based authorization, and automated tests.

## Development Model

All changes should be developed in a dedicated feature, fix, refactor, test, or chore branch and merged into `main` through a Pull Request.

Documentation for feature-level changes is intended to be maintained automatically by the repository documentation workflow.
