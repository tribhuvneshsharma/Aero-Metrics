import logging
import os
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from packages.db.models import Base

logger = logging.getLogger("apix-db")

# Default to zero-config local SQLite if DATABASE_URL not set
DEFAULT_DB_PATH = Path(__file__).resolve().parent.parent.parent / "aerometrics.db"
DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{DEFAULT_DB_PATH}")

# If SQLite, ensure connect_args allows multi-threading
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    """Create all tables in the database and ensure column migrations."""
    Base.metadata.create_all(bind=engine)
    try:
        with engine.connect() as conn:
            from sqlalchemy import text

            res = conn.execute(text("PRAGMA table_info(raw_quotes);")).fetchall()
            cols = [r[1] for r in res]
            if cols and "quote_id" not in cols:
                conn.execute(text("ALTER TABLE raw_quotes ADD COLUMN quote_id TEXT;"))
                conn.commit()
    except Exception as e:
        logger.debug("Database schema check notice: %s", e)


def get_db():
    """Dependency for database sessions."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
