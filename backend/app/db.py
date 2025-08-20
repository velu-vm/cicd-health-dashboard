import os
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.pool import StaticPool
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./data.db")

# Create base class for models
Base = declarative_base()

# Create async engine
async_engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {},
    pool_pre_ping=True,
)

# Create async session factory
AsyncSessionLocal = sessionmaker(
    async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# Create sync engine for migrations and testing
sync_engine = create_engine(
    DATABASE_URL.replace("+aiosqlite", "").replace("+asyncpg", ""),
    echo=False,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {},
    pool_pre_ping=True,
)

# Create sync session factory
SyncSessionLocal = sessionmaker(
    sync_engine,
    expire_on_commit=False,
)

async def init_db():
    """Initialize database tables"""
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

def init_db_sync():
    """Initialize database tables synchronously (for testing)"""
    Base.metadata.create_all(bind=sync_engine)

async def get_db():
    """Dependency to get database session"""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()

def get_db_sync():
    """Get database session synchronously (for testing)"""
    db = SyncSessionLocal()
    try:
        yield db
    finally:
        db.close()
