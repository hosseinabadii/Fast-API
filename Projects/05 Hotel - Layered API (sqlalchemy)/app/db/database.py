from pathlib import Path

from loguru import logger
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .models import Base
from .sample_data import customers, rooms

SQLALCHEMY_DATABASE_URL = "sqlite:///db.sqlite"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


def create_db():
    if not Path("./db.sqlite").exists():
        logger.info("Database not exists. Creating database...")
        Base.metadata.create_all(engine)
        session = SessionLocal()
        session.add_all(customers)
        session.add_all(rooms)
        session.commit()
        session.close()
        logger.info("Database created.")
    else:
        logger.info("Database is already exists.")
