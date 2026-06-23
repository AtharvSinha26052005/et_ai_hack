"""SQLite/SQLAlchemy async database client."""

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from config.settings import settings
import logging

logger = logging.getLogger(__name__)


class Base(DeclarativeBase):
    """SQLAlchemy declarative base for all models."""
    pass


# Async engine
engine = create_async_engine(
    settings.sqlite_url,
    echo=settings.debug,
    connect_args={"check_same_thread": False},  # SQLite-specific
)

# Session factory
async_session_factory = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def init_db() -> None:
    """Create all tables."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("SQLite database initialized")


async def get_session() -> AsyncSession:
    """Dependency for FastAPI — yields an async session."""
    async with async_session_factory() as session:
        yield session


async def close_db() -> None:
    """Dispose engine on shutdown."""
    await engine.dispose()
    logger.info("SQLite connection closed")
