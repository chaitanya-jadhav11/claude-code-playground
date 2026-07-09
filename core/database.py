"""Database configuration and session management for SQLAlchemy."""

import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import Session
from typing import Generator

load_dotenv(override=True)
DATABASE_URL=os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL) # Datasource

session = sessionmaker( # EntityManagerFactory OR session factory.
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base = declarative_base() # Base class for our models. It maintains a catalog of classes and tables relative to that base.
Base = declarative_base()


def get_db() -> Generator[Session, None, None]:
    """Yield a database session and ensure it is closed afterwards.

    Intended for use as a dependency (e.g. with FastAPI's ``Depends``).
    A new session is created per call, yielded to the caller, and closed
    when the caller is done, regardless of whether an error occurred.

    Yields:
        Session: An active SQLAlchemy session bound to the configured engine.
    """
    db = session()
    try:
        yield db
    finally:
        db.close()
    return db






