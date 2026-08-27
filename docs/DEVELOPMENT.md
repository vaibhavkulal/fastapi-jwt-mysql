# Development Guide

## Branches

Use a dedicated branch for every change:

```text
feature/<name>
fix/<name>
refactor/<name>
test/<name>
chore/<name>
```

## Local Checks

Before opening a Pull Request:

```powershell
pytest -q
```

If database models changed, also verify the Alembic migration locally.

## Pull Requests

Pull Requests should target `main` and include:

- A clear description of the change.
- The related issue when applicable.
- Tests for changed behavior.
- A migration when the database schema changes.
- No secrets or `.env` files.

## Documentation

Feature-level documentation is maintained alongside code. The repository's documentation automation is intended to inspect Pull Request changes and update generated documentation when appropriate.
