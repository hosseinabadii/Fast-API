from pathlib import Path

from loguru import logger
from models import Base
from sample_data import customers, rooms
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///db.sqlite"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_db():
    if not Path("./db.sqlite").exists():
        logger.info("Database not exists. Creating database...")
        Base.metadata.create_all(engine)
        db = SessionLocal()
        db.add_all(customers)
        db.add_all(rooms)
        db.commit()
        db.close()
        logger.info("Database created.")
    else:
        logger.info("Database is already exists.")
