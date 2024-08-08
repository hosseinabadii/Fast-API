from pathlib import Path

from config import settings
from loguru import logger
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = settings.sqlalchemy_database_url

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


def init_db():
    if not Path("./db.sqlite").exists():
        logger.info("Database does not exist. Creating database...")
        Base.metadata.create_all(bind=engine)
        logger.info("Database created.")
    else:
        logger.info("Database is already exists.")
