from sqlalchemy.orm import Session
from backend.models.database import get_db


def db_session() -> Session:
    return next(get_db())
