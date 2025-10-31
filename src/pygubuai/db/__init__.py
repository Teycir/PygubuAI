"""Database module for SQLAlchemy integration"""
from pathlib import Path
from typing import Optional
import logging

logger = logging.getLogger(__name__)

try:
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker, Session
    SQLALCHEMY_AVAILABLE = True
except ImportError:
    SQLALCHEMY_AVAILABLE = False
    Session = None
    logger.warning("SQLAlchemy not installed, database features unavailable")

_engine = None
_SessionLocal = None


def get_db_path() -> Path:
    """Get database file path"""
    from ..config import Config
    config = Config()
    return config.config_dir / "pygubuai.db"


def init_db(db_path: Optional[Path] = None) -> bool:
    """Initialize database"""
    if not SQLALCHEMY_AVAILABLE:
        return False

    global _engine, _SessionLocal

    if db_path is None:
        db_path = get_db_path()

    db_path.parent.mkdir(parents=True, exist_ok=True)

    _engine = create_engine(f"sqlite:///{db_path}", echo=False)
    _SessionLocal = sessionmaker(bind=_engine)

    from .models import Base
    Base.metadata.create_all(_engine)

    logger.info(f"Database initialized at {db_path}")
    return True


def get_session() -> Optional[Session]:
    """Get database session"""
    if not SQLALCHEMY_AVAILABLE or _SessionLocal is None:
        return None
    return _SessionLocal()


def close_db():
    """Close database connection"""
    global _engine
    if _engine:
        _engine.dispose()
        _engine = None
