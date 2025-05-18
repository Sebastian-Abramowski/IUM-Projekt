from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from app.ab import AbRepository
from app.db.database import SessionLocal


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


DbDependency = Annotated[Session, Depends(get_db)]


def get_ab_repository(db: DbDependency):
    return AbRepository(db)


AbRepositoryDependency = Annotated[AbRepository, Depends(get_ab_repository)]
