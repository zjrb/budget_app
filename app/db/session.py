import os
from dotenv import load_dotenv, find_dotenv
from sqlalchemy import MetaData, inspect
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session, scoped_session
from sqlalchemy.ext.declarative import declarative_base

load_dotenv(find_dotenv())

SQLALCHEMY_DATABASE_URI = (
    "postgresql+psycopg2://"
    + os.getenv("DB_USER")
    + ":"
    + os.getenv("DB_PASSWORD")
    + "@"
    + os.getenv("DB_HOST")
    + ":5432/"
    + os.getenv("DB_NAME")
)

engine = create_engine(SQLALCHEMY_DATABASE_URI, connect_args={}, future=True, echo=True)

SessionLocal = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine)
)

Base = declarative_base()


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
