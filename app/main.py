from fastapi import Depends, FastAPI
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.database import get_db
from app.routers import auth, users

app = FastAPI(
    title="FastAPI JWT MySQL",
    description="FastAPI + MySQL authentication API with SQLAlchemy and Alembic.",
    version="1.0.0",
)

app.include_router(auth.router)
app.include_router(users.router)


@app.get("/")
def root():
    return {"message": "FastAPI is running"}


@app.get("/db-test")
def database_test(db: Session = Depends(get_db)):
    result = db.execute(text("SELECT 1"))

    return {
        "database": result.scalar()
    }