from config import settings
from sqlmodel import Session, SQLModel, create_engine

DATABASE_URL = settings.database_url

engine = create_engine(DATABASE_URL)


def init_db():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
