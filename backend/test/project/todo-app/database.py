import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.engine import make_url
from sqlalchemy.orm import DeclarativeBase, sessionmaker

load_dotenv()

DATABASE_URI = os.getenv("DATABASE_URI")


def create_database_if_not_exists():
    url = make_url(DATABASE_URI)

    db_name = url.database

    # Connect to the default postgres database
    admin_url = url.set(database="postgres")

    engine = create_engine(
        admin_url,
        isolation_level="AUTOCOMMIT",
    )

    with engine.connect() as conn:
        result = conn.execute(
            text(
                "SELECT 1 FROM pg_database WHERE datname=:name"
            ),
            {"name": db_name},
        )

        exists = result.scalar()

        if not exists:
            conn.execute(text(f'CREATE DATABASE "{db_name}"'))

    engine.dispose()


# Create database automatically
create_database_if_not_exists()

engine = create_engine(DATABASE_URI)

SessionLocal = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    pass


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()