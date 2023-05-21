from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from contextlib import contextmanager

Base = declarative_base()
load_dotenv()

SQLALCHEMY_DATABASE_URL = os.getenv("SQLALCHEMY_DATABASE_URL")
# Create all tables defined in the metadata if they don't exist
engine = create_engine(
    "postgresql://postgres:nndvhGgsQwW9PRxdcbzN@containers-us-west-197.railway.app:6679/railway")


# Create all tables defined in the metadata if they don't exist
Base.metadata.create_all(bind=engine)

# Create a session factory

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@contextmanager
def get_database_connection() -> Session:
    """
    Context manager for handling database connections and transactions.

    Yields:
        Session: A SQLAlchemy database session.

    Raises:
        Any: Any exception raised during the transaction.

    Notes:
        - The session is committed if no exceptions occur.
        - The session is rolled back if an exception occurs.
    """
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except:
        db.rollback()
        raise
    finally:
        db.close()
